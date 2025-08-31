from typing import List, Dict, Any, Optional, Union
import numpy as np
import pandas as pd
import requests

# メタ情報を取得する関数
def get_metainfo(
        appId: str,
        statsDataId: str,
        version: str="3.0",
        timeout: int=10,
    ) -> Dict[str, Any]:
    meta_url = f"https://api.e-stat.go.jp/rest/{version}/app/json/getMetaInfo"
    meta_params = {"appId": appId, "statsDataId": statsDataId}
    try:
        meta_res = requests.get(meta_url, params=meta_params, timeout=timeout)
        meta_res.raise_for_status()
        return meta_res.json()
    except requests.exceptions.HTTPError as e:
        print("HTTPError:", e)
        return {"error": "HTTP request failed"}
    except Exception as e:
        print(f"Exception Error: {e}")
        return {"error": "An unexpected error occurred"}

# 統計データを取得する関数
def get_statsdata(
        appId: str, 
        statsDataId: str, 
        params: Dict[str, Any]=None, 
        version: str="3.0", 
        timeout: int=60
    ) -> Dict[str, Any]:
    if params is None:
        params = {}
    data_url = f"https://api.e-stat.go.jp/rest/{version}/app/json/getStatsData"
    data_params = {"appId": appId, "statsDataId": statsDataId}
    data_params.update(params)
    try:
        data_res = requests.get(data_url, params=data_params, timeout=timeout)
        data_res.raise_for_status()
        return data_res.json()
    except requests.exceptions.HTTPError as e:
        print("HTTPError:", e)
        return {"error": "HTTP request failed"}
    except Exception as e:
        print(f"Exception Error: {e}")
        return {"error": "An unexpected error occurred"}

# 統計データのJSONからDataFrameを抽出する関数
def statsjson_to_dataframe(data: Dict[str, Any]) -> pd.DataFrame:
    value = pd.json_normalize(
        data, 
        record_path=["GET_STATS_DATA", "STATISTICAL_DATA", "DATA_INF", "VALUE"]
    ).rename(
        columns=lambda col: col.lstrip("@").replace("$", "value")
    )
    return value

# 統計データの欠測値をNumPyのNaNに置換する関数
def missing_to_nan(
        value: pd.DataFrame, 
        note: Union[Dict[str, str], List[Dict[str, str]]]
    ) -> pd.DataFrame:
    if isinstance(note, dict):
        note_char = note["@char"]
    elif isinstance(note, list):
        note_char = [n["@char"] for n in note]
    else:
        print(f"引数noteの型は辞書またはリストにしてください。noteの型: {type(note)}")
        return value
    return value.assign(**{
        "value": lambda df: df["value"]
            .replace(note_char, np.nan)
            .astype(float)
    })

# statsjson_to_dataframeとmissing_to_nan、及びメタデータ結合を一括処理する関数
def cleansing_statsdata(data: Dict[str, Any]) -> pd.DataFrame:
    value = statsjson_to_dataframe(data)
    note = data["GET_STATS_DATA"]["STATISTICAL_DATA"]["DATA_INF"].get("NOTE")
    if note:
        value = missing_to_nan(value, note)
    else:
        value = value.assign(**{
            "value": lambda df: df["value"].astype(float)
        })
    class_obj = data["GET_STATS_DATA"]["STATISTICAL_DATA"]["CLASS_INF"]["CLASS_OBJ"]
    for co in class_obj:
        class_entries = co["CLASS"]
        if isinstance(class_entries, list):
            cls_df = pd.DataFrame(class_entries)
        elif isinstance(class_entries, dict):
            cls_df = pd.DataFrame(pd.Series(class_entries)).T
        else:
            print("CLASS_INF>CLASS_OBJ>CLASSの型: ", type(class_entries))
            continue
        cls_df = (cls_df
            .set_index("@code")
            .rename(columns=lambda col: f"{co['@name']}{col.lstrip('@')}")
        )
        value = (value
            .merge(cls_df, left_on=co["@id"], right_index=True, how="left")
            .rename(columns={co["@id"]: f"{co['@name']}code"})
        )
    return value

# 列名を日本語に変換
def colname_to_japanese(value: pd.DataFrame) -> pd.DataFrame:
    # 英語と日本語の対応
    attr_map = {"value": "値", "code": "コード", "name": "", "level": "階層レベル", 
        "unit": "単位", "parentCode": "親コード", "addInf": "追加情報", "tab": "表章項目", 
        "cat": "分類", "area": "地域", "time": "時間軸", "annotation": "注釈記号"  
    }
    def _convert(c):
        for k, v in attr_map.items():
            if k in c:
                return c.replace(k, v)
        return c
    return value.rename(columns=_convert)

# 階層情報を持つDataFrameを作成する関数
def create_hierarchy_dataframe(
        metainfo: Dict[str, Any], 
        cat_key: int,
        level_to: Optional[int]=None
    ) -> pd.DataFrame:
    """
    指定されたメタ情報に基づき、カテゴリの最下層レベルで行が一意となる階層DataFrameを作成する関数
    各行は、各階層のコードと名称を「コード_名称」の形式で保持し、
    欠落している中間階層は前方補完(ffill)で埋められる。

    Parameters
    ----------
    metainfo: Dict[str, Any]
        メタデータ情報。階層情報（@code, @name, @level, @parentCode）が含まれる
    cat_key: int
        対象のカテゴリキー
    level_to: Optional[int]
        階層の最大レベルを指定するオプション引数
    
    Returns
    -------
    pandas.DataFrame
        最下層ノードごとの行を持つ階層DataFrame。
    """
    # 対象カテゴリのメタ情報を取得
    cat_meta = metainfo["GET_META_INFO"]["METADATA_INF"]["CLASS_INF"]["CLASS_OBJ"][cat_key]
    meta_name = cat_meta["@name"]
    meta_cls_df = pd.DataFrame(cat_meta["CLASS"]).assign(
        **{"@level": lambda df: df["@level"].astype(int)}
    )
    # 親コードとして参照されているコードの集合を作成
    parent_codes = set()
    for _, row in meta_cls_df.iterrows():
        parent_code = row.get("@parentCode")
        if parent_code and str(parent_code).strip():
            parent_codes.add(parent_code)
    # 各ノードを@codeで参照する辞書を作成
    code_to_record = {row["@code"]: row for _, row in meta_cls_df.iterrows()}

    def _get_ancestry_chain(meta_record: Dict[str, Any]) -> Dict[int, str]:
        """
        メタ情報の一つのレコード(ノード)の親コードのつながり(チェーン)をたどり取得する関数
        親コードのつながりの辞書(祖先チェーン)を返す。
        
        Parameters
        ----------
        meta_record : Dict[str, Any]
            メタ情報のクラスの1レコード。
            @code, @name, @level, @unit, @parentCodeをキーに含む。

        Returns
        -------
        Dict[int, str]
            階層レベル@levelをキー、対応するコード@codeを値とし、
            親階層をたどる辞書

        Output Example:
        -------
             {4: '273', 3: '020', 2: '019', 1: '018'}
        """
        
        chain = {}
        current_record = meta_record
        while current_record is not None:
            lv = current_record["@level"]
            chain[lv] = current_record["@code"]
            parent_code = current_record.get("@parentCode")
            if not parent_code or parent_code not in code_to_record:
                break
            current_record = code_to_record[parent_code]
        return chain

    # 最深階層(全ノードの中で最も深いレベル)を取得
    max_level = meta_cls_df["@level"].max()
    # 各ノードについて、祖先チェーンを作成
    # ただし、子ノードを持つ親ノードは最終出力から除外する
    chain_rows = []
    for _, row in meta_cls_df.iterrows():
        # row["@code"]が子ノードとして利用されている場合はスキップ
        if row["@code"] in parent_codes:
            continue

        node_level = row["@level"]
        ancestry = _get_ancestry_chain(row)
        row_chain = {}
        last_code = None
        # ノード自身のレベルまでなら、前方補完を実施
        for lv in range(1, max_level + 1):
            col = f"level{lv}"
            if lv <= node_level:
                if lv in ancestry:
                    last_code = ancestry[lv]
                    row_chain[col] = ancestry[lv]
                else:
                    row_chain[col] = last_code  # ffill的処理
            else:
                row_chain[col] = None
        chain_rows.append(row_chain)

    hierarchy_df = pd.DataFrame(chain_rows)

    # 各階層列に対して、対応するコードと名称("code_name")を結合した列をマージ
    for lv in range(1, max_level + 1):
        lv_col = f"level{lv}"
        name_col = f"{meta_name}階層{lv}"
        name_df = meta_cls_df[["@code", "@name"]].rename(
            columns={"@code": lv_col, "@name": name_col}
        )
        name_df[name_col] = name_df[lv_col] + "_" + name_df[name_col]
        hierarchy_df = hierarchy_df.merge(name_df, on=lv_col, how="left")

    # 行内の各level列に対して前方補完(ffill)を実施
    lv_cols = [f"level{lv}" for lv in range(1, max_level + 1)]
    hierarchy_df[lv_cols] = hierarchy_df[lv_cols].ffill(axis=1)
    # "code_name"の列についても、行内で前方補完を実施
    hierarchy_cols = [f"{meta_name}階層{lv}" for lv in range(1, max_level + 1)]
    hierarchy_df[hierarchy_cols] = hierarchy_df[hierarchy_cols].ffill(axis=1)

    if isinstance(level_to, int) and 0 < level_to < max_level:
        # 指定された最大階層レベルまでの列のみを残す
        hierarchy_df = hierarchy_df[
            [f"level{lv}" for lv in range(1, level_to + 1)] +
            [f"{meta_name}階層{lv}" for lv in range(1, level_to + 1)]
        ].drop_duplicates()

    return hierarchy_df
