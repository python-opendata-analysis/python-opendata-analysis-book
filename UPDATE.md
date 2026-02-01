# 正誤表

2026年1月時点で判明している誤植などを掲載しています。 
対応の刷が記載されていない誤植は次回重版時に修正予定です。

| 項番 | 該当箇所 | 誤 | 正 | 対応 | 補足 |
| -- | -- | -- | -- | -- | -- |
| 1 | 106ページ | 統計ダッシュボードAPIのページ94)の | 統計ダッシュボードAPIのページ93)の | 2刷 | 誤植のため |
| 2 | 106ページ | 「【系列要素コードの説明】」の黄色の四角枠の中のリンクにある「～」をクリックしてExcelファイルをダウンロードします | 「【系列要素コードの説明】」の黄色の四角枠の中のリンク「系列コード体系:xlsx」をクリックしてExcelファイルをダウンロードします | 2刷 | 誤植のため |
| 3 | 240ページ脚注 | https://beta.bls.gov/dataQuery/search | https://data.bls.gov/dataQuery/search | 2刷 | 誤植のため |
| 4 | 212ページ | Investors Network | Investors' NETwork | 3刷予定 | 誤植のため |
| 5 | 286ページ | "corporate_type"が株式会社、"year"が2021年のデータをJSON形式で取得します。 | "corporate_type"が株式会社、"year"が2023年のデータをJSON形式で取得します。 | 項番11及び13にて対応 | 誤植のため |
| 6 | 282ページ脚注 | https://info.gbiz.go.jp/resource/index.html | https://help.info.gbiz.go.jp/hc/ja/articles/4795050523806 | 3刷予定 |  サービス提供システムの変更のため |
| 7 | 283ページ | なお、gBizINFO は2026年1月に次期システムに移行し、2025年9月から現行システムのAPI利用申請の受付が中止されます。次期gBizINFOに関する情報ページによると、2025年8月末時点で、2025年8月7日がページ最終更新日となっており、2025年9月にAPI利用申請の受付中止、2026年1月に次期システムのサービスが開始し、2026年9月にREST APIのv1が終了してv2への移行予定と記載されています。また、情報ページにgBizINFOのデータ出典元からのデータ収集の凍結状況についても記載されています。 | なお、gBizINFOは2026年1月にREST APIのv1からv2にシステム移行しました。 | 3刷予定 | サービス提供システムの変更のため |
| 8 | 283ページ脚注 | https://info.gbiz.go.jp/api/index.html | https://content.info.gbiz.go.jp/api/index.html | 3刷予定 | サービス提供システムの変更のため |
| 9 | 285ページ | 本節冒頭で説明したように gBizINFO は 2026 年 1 月に次期システムに移行し、2025 年 9 月から現行システムの API 利用申請の受付が中止されます。本書のサポートサイト（1.3.3 項に記載）にて、2026 年 1 月以降に、次期システムの仕様に対応した修正コードを提供予定です。以下では、API 利用申請の受付が停止している旧システムの仕様にもとづいて gBizINFO の API を紹介します。 | 本節冒頭で説明したように gBizINFOは2026年1月にREST APIのv1からv2にシステム移行しました。本書のサポートサイト（1.3.3 項に記載）にて、現在、v2の仕様に対応したコードを提供しています。 | 3刷予定 | サービス提供システムの変更のため |
| 10 | 285ページ脚注 | https://info.gbiz.go.jp/api/index.html | https://content.info.gbiz.go.jp/api/index.html | 3刷予定 | サービス提供システムの変更のため |
| 11 | 286ページ | "corporate_type"が株式会社、"year"が2021年のデータをJSON形式で取得します。 | "corporate_type"が株式会社のデータをJSON形式で取得します。 | 3刷予定 | サービス提供システムの変更のため |
| 12 | 286ページ | url_hojin = "https://info.gbiz.go.jp/hojin/v1/hojin" | url_hojin = "https://api.info.gbiz.go.jp/hojin/v2/hojin" | 3刷予定 | サービス提供システムの変更のため |
| 13 | 286ページ(コードのparams_hojin内) | "year": "2023",  # 年度 | 削除 | 3刷予定 | サービス提供システムの変更のため |
| 14 | 286ページ脚注 | https://info.gbiz.go.jp/hojin/swagger-ui/index.html#/gBizINFO%20REST%20API/searchInfo | https://api.info.gbiz.go.jp/hojin/swagger-ui/index.html?urls.primaryName=v2 | 3刷予定 | サービス提供システムの変更のため |
| 15 | 289ページ | url_hojin = "https://info.gbiz.go.jp/hojin/v1/hojin" | url_hojin = "https://api.info.gbiz.go.jp/hojin/v2/hojin" | 3刷予定 | サービス提供システムの変更のため |
| 16 | 291ページ | なお、gBizINFOでは2026 年 1 月から次期システムに移行することがWebサイト上でアナウンスされています。本書が出版される2025年10月段階ではAPI利用申請の受付が中止されています。そのため、代替案としてCSVデータを用いてデータを取得する2つの方法を以下に示します。 | なお、gBizINFOのAPIを利用せずに、CSVデータを用いてデータを取得する2つの方法を以下に示します。 | 3刷予定 | サービス提供システムの変更のため |
| 17 | 91ページ | meta["GET_META_INFO"]["METADATA_INF"]["TABLE_INF"].keys() | meta["GET_META_INFO"]["METADATA_INF"].keys() | 4刷予定 | 文章のわかりやすさのため |
| 18 | 91ページ | dict_keys(['@id', 'STAT_NAME', 'GOV_ORG', 'STATISTICS_NAME', 'TITLE', 'CYCLE', 'SURVEY_DATE', 'OPEN_DATE', 'SMALL_AREA', 'COLLECT_AREA', 'MAIN_CATEGORY', 'SUB_CATEGORY', 'OVERALL_TOTAL_NUMBER', 'UPDATED_DATE', 'STATISTICS_NAME_SPEC', 'DESCRIPTION', 'TITLE_SPEC']) | dict_keys(['TABLE_INF', 'CLASS_INF']) | 4刷予定 | 文章のわかりやすさのため |
| 19 | 91ページ | 辞書のkeysメソッドで1つずつキーを確認すると | 辞書のkeysメソッドと添字演算子[]で"GET_META_INFO"から1つずつキーを確認すると | 4刷予定 | 文章のわかりやすさのため |
| 20 | 91ページ図6.7 | メタ情報のJSON構造 | メタ情報のJSON構造（本書で利用する主要なキーを抜粋） | 4刷予定 | 文章のわかりやすさのため |
| 21 | 96ページ | 辞書のkeysメソッドで1つずつキーを確認すると | 辞書のkeysメソッドと添字演算子[]で"GET_STATS_INFO"から1つずつキーを確認すると | 4刷予定 | 文章のわかりやすさのため |
| 22 | 96ページ図6.8 | 統計データのJSON構造 | 統計データのJSON構造（本書で利用する主要なキーを抜粋） | 4刷予定 | 文章のわかりやすさのため |

# 更新情報

- 2025-10-19: サポートサイト公開
- 2025-10-24: 書籍発売
- 2025-12-3: 重版第2刷
- 2025-12-28: 第1刷正誤表更新(第2刷対応)
- 2026-1-31: gBizINFO REST APIのv1からv2への移行に対応。第2刷正誤表更新(第3刷対応)
- 2026-2-19: 重版第3刷

## Issue対応

- 2025/11/1: 第7章 ch07_population.ipynbのリポジトリ側での変数名の脱字(vital_value_df)の修正　(Issue #11)
