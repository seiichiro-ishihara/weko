insert into
    item_type_property (
        created,
        updated,
        id,
        name,
        schema,
        form,
        forms,
        delflg,
        sort
    )
values
    (
        CURRENT_TIMESTAMP,
        CURRENT_TIMESTAMP,
        (select max(id) + 1 from item_type_property where id < 10000),
        'Billing file',
        '{"type":"object","format":"object","properties":{"url":{"type":"object","title":"本文URL","format":"object","properties":{"url":{"type":"string","title":"本文URL","format":"text","title_i18n":{"en":"","ja":""}},"label":{"type":"string","title":"ラベル","format":"text","title_i18n":{"en":"","ja":""}},"objectType":{"enum":[null,"abstract","summary","fulltext","thumbnail","other"],"type":"string","title":"オブジェクトタイプ","format":"select","currentEnum":["abstract","summary","fulltext","thumbnail","other"]}}},"date":{"type":"array","items":{"type":"object","format":"object","properties":{"dateType":{"enum":[],"type":"string","title":"日付タイプ","format":"select","currentEnum":[]},"dateValue":{"type":"string","title":"日付","format":"datetime","title_i18n":{"en":"","ja":""}}}},"title":"オープンアクセスの日付","format":"array"},"format":{"type":"string","title":"フォーマット","format":"text","title_i18n":{"en":"","ja":""}},"version":{"type":"string","title":"バージョン情報","format":"text","title_i18n":{"en":"","ja":""}},"fileDate":{"type":"array","items":{"type":"object","format":"object","properties":{"fileDateType":{"enum":[null,"Accepted","Collected","Copyrighted","Created","Issued","Submitted","Updated","Valid"],"type":["null","string"],"title":"日付タイプ","format":"select","currentEnum":["Accepted","Collected","Copyrighted","Created","Issued","Submitted","Updated","Valid"]},"fileDateValue":{"type":"string","title":"日付","format":"datetime","title_i18n":{"en":"","ja":""}}}},"title":"日付","format":"array"},"filename":{"enum":[],"type":["null","string"],"title":"表示名","format":"text","title_i18n":{"en":"","ja":""}},"filesize":{"type":"array","items":{"type":"object","format":"object","properties":{"value":{"type":"string","title":"サイズ","format":"text","title_i18n":{"en":"","ja":""}}}},"title":"サイズ","format":"array"},"accessrole":{"enum":["","open_access","open_date","open_login","open_no"],"type":"string","title":"アクセス","format":"radios"},"displaytype":{"enum":[null,"detail","simple","preview"],"type":["null","string"],"title":"表示形式","format":"select"},"licensefree":{"type":"string","title":"自由ライセンス","format":"textarea","title_i18n":{"en":"","ja":""}},"licensetype":{"enum":[],"type":["null","string"],"title":"ライセンス","format":"select"},"billing":{"type":"array","format":"checkboxes","enum":["billing_file"],"items":{"type":"string","enum":["billing_file"]},"title":"課金"},"role":{"type":"array","format":"array","items":{"type":"object","format":"object","properties":{"role":{"type":"array","format":"select","enum":[],"currentEnum":[],"title":"ロール"}}},"title":"ロール"},"priceinfo":{"type":"array","format":"array","items":{"type":"object","format":"object","properties":{"billingrole":{"type":"array","format":"select","enum":[],"currentEnum":[],"title":"ロール"},"tax":{"type":"string","format":"checkboxes","enum":["include_tax"],"items":{"type":"string","enum":["include_tax"]},"title":"税"},"price":{"type":"string","format":"text","title":"価格"}}},"title":"価格情報"}}}',
        '{"key":"parentkey","type":"fieldset","items":[{"key":"parentkey.filename","type":"template","title":"表示名","onChange":"fileNameSelect(this, form, modelValue)","titleMap":[],"title_i18n":{"en":"FileName","ja":"表示名"},"templateUrl":"/static/templates/weko_deposit/datalist.html","fieldHtmlClass":"file-name"},{"key":"parentkey.url","type":"fieldset","items":[{"key":"parentkey.url.url","type":"text","title":"本文URL","feedback":false,"title_i18n":{"en":"Text URL","ja":"本文URL"},"fieldHtmlClass":"file-text-url","disableSuccessState":true},{"key":"parentkey.url.label","type":"text","title":"ラベル","feedback":false,"title_i18n":{"en":"Label","ja":"ラベル"},"disableSuccessState":true},{"key":"parentkey.url.objectType","type":"select","title":"オブジェクトタイプ","feedback":false,"titleMap":[{"name":"abstract","value":"abstract"},{"name":"summary","value":"summary"},{"name":"fulltext","value":"fulltext"},{"name":"thumbnail","value":"thumbnail"},{"name":"other","value":"other"}],"title_i18n":{"en":"Object Type","ja":"オブジェクトタイプ"},"disableSuccessState":true}],"title":"本文URL","title_i18n":{"en":"Text URL","ja":"本文URL"}},{"key":"parentkey.format","type":"text","title":"フォーマット","title_i18n":{"en":"Format","ja":"フォーマット"}},{"add":"New","key":"parentkey.filesize","items":[{"key":"parentkey.filesize[].value","type":"text","title":"サイズ","title_i18n":{"en":"Size","ja":"サイズ"}}],"style":{"add":"btn-success"},"title":"サイズ","title_i18n":{"en":"Size","ja":"サイズ"}},{"add":"New","key":"parentkey.fileDate","items":[{"key":"parentkey.fileDate[].fileDateType","type":"select","title":"日付タイプ","titleMap":[{"name":"Accepted","value":"Accepted"},{"name":"Collected","value":"Collected"},{"name":"Copyrighted","value":"Copyrighted"},{"name":"Created","value":"Created"},{"name":"Issued","value":"Issued"},{"name":"Submitted","value":"Submitted"},{"name":"Updated","value":"Updated"},{"name":"Valid","value":"Valid"}],"title_i18n":{"en":"Date Type","ja":"日付タイプ"}},{"key":"parentkey.fileDate[].fileDateValue","type":"template","title":"日付","format":"yyyy-MM-dd","title_i18n":{"en":"Date","ja":"日付"},"templateUrl":"/static/templates/weko_deposit/datepicker_multi_format.html"}],"style":{"add":"btn-success"},"title":"日付","title_i18n":{"en":"Date","ja":"日付"}},{"key":"parentkey.version","type":"text","title":"バージョン情報","title_i18n":{"en":"Version Information","ja":"バージョン情報"}},{"key":"parentkey.displaytype","type":"select","title":"表示形式","titleMap":[{"name":"詳細表示","value":"detail","name_i18n":{"en":"Detail","ja":"詳細表示"}},{"name":"簡易表示","value":"simple","name_i18n":{"en":"Simple","ja":"簡易表示"}},{"name":"プレビュー","value":"preview","name_i18n":{"en":"Preview","ja":"プレビュー"}}],"title_i18n":{"en":"Preview","ja":"表示形式"}},{"key":"parentkey.licensetype","type":"select","title":"ライセンス","titleMap":[],"title_i18n":{"en":"License","ja":"ライセンス"}},{"key":"parentkey.licensefree","type":"textarea","notitle":true,"condition":"model.parentkey.licensetype == ''license_free''"},{"type":"template","title":"剽窃チェック","template":"<div class=''text-center'' style=''display:none;''><a class=''btn btn-primary'' href=''/ezas/pdf-detect-weko.html'' target=''_blank'' role=''button''>{{ form.title }}</a></div>","title_i18n":{"en":"Check Plagiarism","ja":"剽窃チェック"}},{"key":"parentkey.accessrole","type":"radios","title":"アクセス","titleMap":[{"name":"オープンアクセス","value":"open_access","name_i18n":{"en":"Open access","ja":"オープンアクセス"}},{"name":"オープンアクセス日を指定する","value":"open_date","name_i18n":{"en":"Input Open Access Date","ja":"オープンアクセス日を指定する"}},{"name":"ログインユーザのみ","value":"open_login","name_i18n":{"en":"Registered User Only","ja":"ログインユーザのみ"}},{"name":"公開しない","value":"open_no","name_i18n":{"en":"Do not Publish","ja":"公開しない"}}],"title_i18n":{"en":"Access","ja":"アクセス"}},{"key":"parentkey.date[0].dateValue","type":"template","title":"公開日","format":"yyyy-MM-dd","condition":"model.parentkey.accessrole == ''open_date''","title_i18n":{"en":"Opendate","ja":"公開日"},"templateUrl":"/static/templates/weko_deposit/datepicker.html"},{"key":"parentkey.billing","type":"template","templateUrl":"/static/templates/weko_deposit/checkboxes.html","condition":"model.parentkey.accessrole == ''open_date'' || model.parentkey.accessrole == ''open_login''","title":"課金","titleMap":[{"value":"billing_file","name":"課金ファイル","name_i18n":{"en":"Billing file","ja":"課金ファイル"}}],"title_i18n":{"en":"Billing","ja":"課金"}},{"key":"parentkey.role","add":"New","style":{"add":"btn-success"},"condition":"model.parentkey.accessrole == ''open_login'' && model.parentkey.billing != ''billing_file''","title":"ロール","items":[{"key":"parentkey.role[].role","type":"select","title":"ロール","titleMap":[],"title_i18n":{"en":"Role","ja":"ロール"}}],"title_i18n":{"en":"Role","ja":"ロール"}},{"key":"parentkey.priceinfo","add":"New","style":{"add":"btn-success"},"condition":"(model.parentkey.accessrole == ''open_date'' || model.parentkey.accessrole == ''open_login'') && model.parentkey.billing == ''billing_file''","title":"価格情報","items":[{"key":"parentkey.priceinfo[].billingrole","type":"select","title":"ロール","titleMap":[],"title_i18n":{"en":"Role","ja":"ロール"}},{"key":"parentkey.priceinfo[].tax","type":"template","templateUrl":"/static/templates/weko_deposit/checkboxes.html","title":"税","titleMap":[{"value":"include_tax","name":"税込","name_i18n":{"en":"Include tax","ja":"税込"}}],"title_i18n":{"en":"Tax","ja":"税"}},{"key":"parentkey.priceinfo[].price","type":"text","title":"価格","title_i18n":{"en":"Price","ja":"価格"}}],"title_i18n":{"en":"Price","ja":"価格情報"}}],"title_i18n":{"en":"Billing file","ja":"課金ファイル"}}',
        '{"add":"New","key":"parentkey","items":[{"key":"parentkey[].filename","type":"template","title":"表示名","onChange":"fileNameSelect(this, form, modelValue)","titleMap":[],"title_i18n":{"en":"FileName","ja":"表示名"},"templateUrl":"/static/templates/weko_deposit/datalist.html","fieldHtmlClass":"file-name"},{"key":"parentkey[].url","type":"fieldset","items":[{"key":"parentkey[].url.url","type":"text","title":"本文URL","feedback":false,"title_i18n":{"en":"Text URL","ja":"本文URL"},"fieldHtmlClass":"file-text-url","disableSuccessState":true},{"key":"parentkey[].url.label","type":"text","title":"ラベル","feedback":false,"title_i18n":{"en":"Label","ja":"ラベル"},"disableSuccessState":true},{"key":"parentkey[].url.objectType","type":"select","title":"オブジェクトタイプ","feedback":false,"titleMap":[{"name":"abstract","value":"abstract"},{"name":"summary","value":"summary"},{"name":"fulltext","value":"fulltext"},{"name":"thumbnail","value":"thumbnail"},{"name":"other","value":"other"}],"title_i18n":{"en":"Object Type","ja":"オブジェクトタイプ"},"disableSuccessState":true}],"title":"本文URL","title_i18n":{"en":"Text URL","ja":"本文URL"}},{"key":"parentkey[].format","type":"text","title":"フォーマット","title_i18n":{"en":"Format","ja":"フォーマット"}},{"add":"New","key":"parentkey[].filesize","items":[{"key":"parentkey[].filesize[].value","type":"text","title":"サイズ","title_i18n":{"en":"Size","ja":"サイズ"}}],"style":{"add":"btn-success"},"title":"サイズ","title_i18n":{"en":"Size","ja":"サイズ"}},{"add":"New","key":"parentkey[].fileDate","items":[{"key":"parentkey[].fileDate[].fileDateType","type":"select","title":"日付タイプ","titleMap":[{"name":"Accepted","value":"Accepted"},{"name":"Collected","value":"Collected"},{"name":"Copyrighted","value":"Copyrighted"},{"name":"Created","value":"Created"},{"name":"Issued","value":"Issued"},{"name":"Submitted","value":"Submitted"},{"name":"Updated","value":"Updated"},{"name":"Valid","value":"Valid"}],"title_i18n":{"en":"Date Type","ja":"日付タイプ"}},{"key":"parentkey[].fileDate[].fileDateValue","type":"template","title":"日付","format":"yyyy-MM-dd","title_i18n":{"en":"Date","ja":"日付"},"templateUrl":"/static/templates/weko_deposit/datepicker_multi_format.html"}],"style":{"add":"btn-success"},"title":"日付","title_i18n":{"en":"Date","ja":"日付"}},{"key":"parentkey[].version","type":"text","title":"バージョン情報","title_i18n":{"en":"Version Information","ja":"バージョン情報"}},{"key":"parentkey[].displaytype","type":"select","title":"表示形式","titleMap":[{"name":"詳細表示","value":"detail","name_i18n":{"en":"Detail","ja":"詳細表示"}},{"name":"簡易表示","value":"simple","name_i18n":{"en":"Simple","ja":"簡易表示"}},{"name":"プレビュー","value":"preview","name_i18n":{"en":"Preview","ja":"プレビュー"}}],"title_i18n":{"en":"Preview","ja":"表示形式"}},{"key":"parentkey[].licensetype","type":"select","title":"ライセンス","titleMap":[],"title_i18n":{"en":"License","ja":"ライセンス"}},{"key":"parentkey[].licensefree","type":"textarea","notitle":true,"condition":"model.parentkey[arrayIndex].licensetype == ''license_free''"},{"type":"template","title":"剽窃チェック","template":"<div class=''text-center'' style=''display:none;''><a class=''btn btn-primary'' href=''/ezas/pdf-detect-weko.html'' target=''_blank'' role=''button''>{{ form.title }}</a></div>","title_i18n":{"en":"Check Plagiarism","ja":"剽窃チェック"}},{"key":"parentkey[].accessrole","type":"radios","title":"アクセス","titleMap":[{"name":"オープンアクセス","value":"open_access","name_i18n":{"en":"Open access","ja":"オープンアクセス"}},{"name":"オープンアクセス日を指定する","value":"open_date","name_i18n":{"en":"Input Open Access Date","ja":"オープンアクセス日を指定する"}},{"name":"ログインユーザのみ","value":"open_login","name_i18n":{"en":"Registered User Only","ja":"ログインユーザのみ"}},{"name":"公開しない","value":"open_no","name_i18n":{"en":"Do not Publish","ja":"公開しない"}}],"title_i18n":{"en":"Access","ja":"アクセス"}},{"key":"parentkey[].date[0].dateValue","type":"template","title":"公開日","format":"yyyy-MM-dd","condition":"model.parentkey[arrayIndex].accessrole == ''open_date''","title_i18n":{"en":"Opendate","ja":"公開日"},"templateUrl":"/static/templates/weko_deposit/datepicker.html"},{"key":"parentkey[].billing","type":"template","templateUrl":"/static/templates/weko_deposit/checkboxes.html","condition":"model.parentkey[arrayIndex].accessrole == ''open_date'' || model.parentkey[arrayIndex].accessrole == ''open_login''","title":"課金","titleMap":[{"value":"billing_file","name":"課金ファイル","name_i18n":{"en":"Billing file","ja":"課金ファイル"}}],"title_i18n":{"en":"Billing","ja":"課金"}},{"key":"parentkey[].role","add":"New","style":{"add":"btn-success"},"condition":"model.parentkey[arrayIndex].accessrole == ''open_login'' && model.parentkey[arrayIndex].billing != ''billing_file''","title":"ロール","items":[{"key":"parentkey[].role[].role","type":"select","title":"ロール","titleMap":[],"title_i18n":{"en":"Role","ja":"ロール"}}],"title_i18n":{"en":"Role","ja":"ロール"}},{"key":"parentkey[].priceinfo","add":"New","style":{"add":"btn-success"},"condition":"(model.parentkey[arrayIndex].accessrole == ''open_date'' || model.parentkey[arrayIndex].accessrole == ''open_login'') && model.parentkey[arrayIndex].billing == ''billing_file''","title":"価格情報","items":[{"key":"parentkey[].priceinfo[].billingrole","type":"select","title":"ロール","titleMap":[],"title_i18n":{"en":"Role","ja":"ロール"}},{"key":"parentkey[].priceinfo[].tax","type":"template","templateUrl":"/static/templates/weko_deposit/checkboxes.html","title":"税","titleMap":[{"value":"include_tax","name":"税込","name_i18n":{"en":"Include tax","ja":"税込"}}],"title_i18n":{"en":"Tax","ja":"税"}},{"key":"parentkey[].priceinfo[].price","type":"text","title":"価格","title_i18n":{"en":"Price","ja":"価格"}}],"title_i18n":{"en":"Price","ja":"価格情報"}}],"style":{"add":"btn-success"},"title_i18n":{"en":"Billing file","ja":"課金ファイル"}}',
        false,
        null
    ),
    (
        CURRENT_TIMESTAMP,
        CURRENT_TIMESTAMP,
        (select max(id) + 2 from item_type_property where id < 10000),
        'Restricted access billing file',
        '{"type":"object","format":"object","properties":{"url":{"type":"object","title":"本文URL","format":"object","properties":{"url":{"type":"string","title":"本文URL","format":"text","title_i18n":{"en":"","ja":""}},"label":{"type":"string","title":"ラベル","format":"text"},"objectType":{"enum":[null,"abstract","dataset","fulltext","software","summary","thumbnail","other"],"type":"string","title":"オブジェクトタイプ","format":"select"}}},"terms":{"enum":[],"type":["string","number","null"],"title":"利用規約","format":"select"},"format":{"type":"string","title":"フォーマット","format":"text"},"provide":{"type":"array","items":{"type":"object","format":"object","properties":{"role":{"enum":[],"type":["string","number","null"],"title":"ロール","format":"select","currentEnum":[]},"workflow":{"enum":[],"type":["string","number","null"],"title":"ワークフロー","format":"select","currentEnum":[]}}},"title":"提供方法","format":"array"},"version":{"type":"string","title":"バージョン情報","format":"text"},"dataType":{"enum":["life","accumulation","combinational_analysis","perfectures","location_information"],"type":["string","null"],"title":"データタイプ","format":"select"},"fileDate":{"type":"array","items":{"type":"object","format":"object","properties":{"fileDateType":{"enum":[null,"Accepted","Collected","Copyrighted","Issued","Submitted","Updated","Valid"],"type":["null","string"],"title":"日付タイプ","format":"select"},"fileDateValue":{"type":"string","title":"日付","format":"datetime"}}},"title":"日付","format":"array"},"filename":{"enum":[],"type":"string","title":"表示名","format":"select"},"filesize":{"type":"array","items":{"type":"object","format":"object","properties":{"value":{"type":"string","title":"サイズ","format":"text"}}},"title":"サイズ","format":"array"},"accessdate":{"type":"string","title":"公開日","format":"datetime"},"accessrole":{"enum":["open_access","open_date","open_login","open_no","open_restricted"],"type":"string","title":"アクセス","format":"radios","default":"open_restricted"},"displaytype":{"enum":["detail","simple","preview"],"type":"string","title":"表示形式","format":"select"},"licensefree":{"type":"string","title":" ","format":"textarea"},"licensetype":{"enum":[],"type":"string","title":"ライセンス","format":"select"},"termsDescription":{"type":"string","title":" ","format":"textarea","title_i18n":{"en":"","ja":""}},"billing":{"type":"array","format":"checkboxes","enum":["billing_file"],"items":{"type":"string","enum":["billing_file"]},"title":"課金"},"role":{"type":"array","format":"array","items":{"type":"object","format":"object","properties":{"role":{"type":"array","format":"select","enum":[],"currentEnum":[],"title":"ロール"}}},"title":"ロール"},"priceinfo":{"type":"array","format":"array","items":{"type":"object","format":"object","properties":{"billingrole":{"type":"array","format":"select","enum":[],"currentEnum":[],"title":"ロール"},"tax":{"type":"string","format":"checkboxes","enum":["include_tax"],"items":{"type":"string","enum":["include_tax"]},"title":"税"},"price":{"type":"string","format":"text","title":"価格"}}},"title":"価格情報"}}}',
        '{"key":"parentkey","type":"fieldset","items":[{"key":"parentkey.filename","type":"template","title":"表示名","onChange":"fileNameSelect(this, form, modelValue)","titleMap":[],"title_i18n":{"en":"FileName","ja":"表示名"},"templateUrl":"/static/templates/weko_deposit/datalist.html"},{"key":"parentkey.url.url","type":"text","title":"本文URL","feedback":false,"title_i18n":{"en":"Text URL","ja":"本文URL"},"fieldHtmlClass":"file-text-url","disableSuccessState":true},{"key":"parentkey.url.label","type":"text","title":"ラベル","feedback":false,"title_i18n":{"en":"Label","ja":"ラベル"},"disableSuccessState":true},{"key":"parentkey.url.objectType","type":"select","title":"オブジェクトタイプ","feedback":false,"titleMap":[{"name":"abstract","value":"abstract","name_i18n":{"en":"abstract","ja":"abstract"}},{"name":"dataset","value":"dataset","name_i18n":{"en":"dataset","ja":"dataset"}},{"name":"fulltext","value":"fulltext","name_i18n":{"en":"fulltext","ja":"fulltext"}},{"name":"software","value":"software","name_i18n":{"en":"software","ja":"software"}},{"name":"summary","value":"summary","name_i18n":{"en":"summary","ja":"summary"}},{"name":"thumbnail","value":"thumbnail","name_i18n":{"en":"thumbnail","ja":"thumbnail"}},{"name":"other","value":"other","name_i18n":{"en":"other","ja":"other"}}],"title_i18n":{"en":"Object Type","ja":"オブジェクトタイプ"},"disableSuccessState":true},{"key":"parentkey.format","type":"text","title":"フォーマット","title_i18n":{"en":"Format","ja":"フォーマット"}},{"add":"New","key":"parentkey.filesize","items":[{"key":"parentkey.filesize[].value","type":"text","title":"サイズ","title_i18n":{"en":"Size","ja":"サイズ"}}],"style":{"add":"btn-success"},"title":"サイズ","title_i18n":{"en":"Size","ja":"サイズ"}},{"add":"New","key":"parentkey.fileDate","items":[{"key":"parentkey.fileDate[].fileDateType","type":"select","title":"日付タイプ","titleMap":[{"name":"Accepted","value":"Accepted"},{"name":"Collected","value":"Collected"},{"name":"Copyrighted","value":"Copyrighted"},{"name":"Issued","value":"Issued"},{"name":"Submitted","value":"Submitted"},{"name":"Updated","value":"Updated"},{"name":"Valid","value":"Valid"}],"title_i18n":{"en":"Date Type","ja":"日付タイプ"}},{"key":"parentkey.fileDate[].fileDateValue","type":"template","title":"日付","format":"yyyy-MM-dd","title_i18n":{"en":"Date","ja":"日付"},"templateUrl":"/static/templates/weko_deposit/datepicker.html"}],"style":{"add":"btn-success"},"title":"日付","title_i18n":{"en":"Date","ja":"日付"}},{"key":"parentkey.version","type":"text","title":"バージョン情報","title_i18n":{"en":"Version Information","ja":"バージョン情報"}},{"key":"parentkey.displaytype","type":"select","title":"表示形式","titleMap":[{"name":"詳細表示","value":"detail","name_i18n":{"en":"Detail","ja":"詳細表示"}},{"name":"簡易表示","value":"simple","name_i18n":{"en":"Simple","ja":"簡易表示"}},{"name":"プレビュー","value":"preview","name_i18n":{"en":"Preview","ja":"プレビュー"}}],"title_i18n":{"en":"Preview","ja":"表示形式"}},{"key":"parentkey.licensetype","type":"select","title":"ライセンス","titleMap":[],"title_i18n":{"en":"License","ja":"ライセンス"}},{"key":"parentkey[].licensefree","type":"textarea","title":" ","condition":"model.parentkey.licensetype == ''license_free''"},{"key":"parentkey.accessrole","type":"radios","title":"アクセス","default":"open_restricted","titleMap":[{"name":"オープンアクセス","value":"open_access","name_i18n":{"en":"Open Access","ja":"オープンアクセス"}},{"name":"オープンアクセス日を指定する","value":"open_date","name_i18n":{"en":"Input Open Access Date","ja":"オープンアクセス日を指定する"}},{"name":"ログインユーザのみ","value":"open_login","name_i18n":{"en":"Registered User Only","ja":"ログインユーザのみ"}},{"name":"公開しない","value":"open_no","name_i18n":{"en":"Do Not Publish","ja":"公開しない"}},{"name":"制限公開","value":"open_restricted","name_i18n":{"en":"Limited Access","ja":"制限公開"}}],"title_i18n":{"en":"Access","ja":"アクセス"}},{"key":"parentkey.accessdate","type":"template","title":"公開日","format":"yyyy-MM-dd","condition":"model.parentkey[arrayIndex].accessrole == ''open_date''","title_i18n":{"en":"Opendate","ja":"公開日"},"templateUrl":"/static/templates/weko_deposit/datepicker.html"},{"key":"parentkey.role","add":"New","style":{"add":"btn-success"},"condition":"model.parentkey.accessrole == ''open_login'' && model.parentkey.billing != ''billing_file''","title":"ロール","items":[{"key":"parentkey.role[].role","type":"select","title":"ロール","titleMap":[],"title_i18n":{"en":"Role","ja":"ロール"}}],"title_i18n":{"en":"Role","ja":"ロール"}},{"key":"parentkey.dataType","type":"select","title":"データタイプ","titleMap":[{"name":"Life","value":"life","name_i18n":{"en":"Life","ja":"ライフ"}},{"name":"Accumulation","value":"accumulation","name_i18n":{"en":"Accumulation","ja":"累積"}},{"name":"Combinational Analysis","value":"combinational_analysis","name_i18n":{"en":"Combinational Analysis","ja":"組合せ分析"}},{"name":"Perfectures","value":"perfectures","name_i18n":{"en":"Perfectures","ja":"都道府県"}},{"name":"Location Information","value":"location_information","name_i18n":{"en":"Location Information","ja":"地点情報"}}],"condition":"model.parentkey.accessrole == ''open_restricted''","title_i18n":{"en":"Data Type","ja":"データタイプ"}},{"add":"New","key":"parentkey.provide","items":[{"key":"parentkey.provide[].workflow","type":"select","title":"ワークフロー","titleMap":[],"title_i18n":{"en":"WorkFlow","ja":"ワークフロー"}},{"key":"parentkey.provide[].role","type":"select","title":"ロール","titleMap":[],"title_i18n":{"en":"Role","ja":"ロール"}}],"style":{"add":"btn-success"},"title":"提供方法","condition":"model.parentkey.accessrole == ''open_restricted''","title_i18n":{"en":"Providing Method","ja":"提供方法"}},{"key":"parentkey.terms","type":"select","title":"利用規約","titleMap":[],"condition":"model.parentkey.accessrole == ''open_restricted''","title_i18n":{"en":"Terms and Conditions","ja":"利用規約"}},{"key":"parentkey.termsDescription","type":"textarea","title":" ","condition":"model.parentkey.accessrole == ''open_restricted'' && model.parentkey.terms== ''term_free''"},{"key":"parentkey.billing","type":"template","templateUrl":"/static/templates/weko_deposit/checkboxes.html","condition":"model.parentkey.accessrole == ''open_date'' || model.parentkey.accessrole == ''open_login''","title":"課金","titleMap":[{"value":"billing_file","name":"課金ファイル","name_i18n":{"en":"Billing file","ja":"課金ファイル"}}],"title_i18n":{"en":"Billing","ja":"課金"}},{"key":"parentkey.priceinfo","add":"New","style":{"add":"btn-success"},"condition":"(model.parentkey.accessrole == ''open_date'' || model.parentkey.accessrole == ''open_login'') && model.parentkey.billing == ''billing_file''","title":"価格情報","items":[{"key":"parentkey.priceinfo[].billingrole","type":"select","title":"ロール","titleMap":[],"title_i18n":{"en":"Role","ja":"ロール"}},{"key":"parentkey.priceinfo[].tax","type":"template","templateUrl":"/static/templates/weko_deposit/checkboxes.html","title":"税","titleMap":[{"value":"include_tax","name":"税込","name_i18n":{"en":"Include tax","ja":"税込"}}],"title_i18n":{"en":"Tax","ja":"税"}},{"key":"parentkey.priceinfo[].price","type":"text","title":"価格","title_i18n":{"en":"Price","ja":"価格"}}],"title_i18n":{"en":"Price","ja":"価格情報"}}],"title_i18n":{"en":"Restricted Access Billing File","ja":"制限公開課金ファイル"}}',
        '{"add":"New","key":"parentkey","items":[{"key":"parentkey[].filename","type":"template","title":"表示名","onChange":"fileNameSelect(this, form, modelValue)","titleMap":[],"title_i18n":{"en":"FileName","ja":"表示名"},"templateUrl":"/static/templates/weko_deposit/datalist.html"},{"key":"parentkey[].url.url","type":"text","title":"本文URL","feedback":false,"title_i18n":{"en":"Text URL","ja":"本文URL"},"fieldHtmlClass":"file-text-url","disableSuccessState":true},{"key":"parentkey[].url.label","type":"text","title":"ラベル","feedback":false,"title_i18n":{"en":"Label","ja":"ラベル"},"disableSuccessState":true},{"key":"parentkey[].url.objectType","type":"select","title":"オブジェクトタイプ","feedback":false,"titleMap":[{"name":"abstract","value":"abstract","name_i18n":{"en":"abstract","ja":"abstract"}},{"name":"dataset","value":"dataset","name_i18n":{"en":"dataset","ja":"dataset"}},{"name":"fulltext","value":"fulltext","name_i18n":{"en":"fulltext","ja":"fulltext"}},{"name":"software","value":"software","name_i18n":{"en":"software","ja":"software"}},{"name":"summary","value":"summary","name_i18n":{"en":"summary","ja":"summary"}},{"name":"thumbnail","value":"thumbnail","name_i18n":{"en":"thumbnail","ja":"thumbnail"}},{"name":"other","value":"other","name_i18n":{"en":"other","ja":"other"}}],"title_i18n":{"en":"Object Type","ja":"オブジェクトタイプ"},"disableSuccessState":true},{"key":"parentkey[].format","type":"text","title":"フォーマット","title_i18n":{"en":"Format","ja":"フォーマット"}},{"add":"New","key":"parentkey[].filesize","items":[{"key":"parentkey[].filesize[].value","type":"text","title":"サイズ","title_i18n":{"en":"Size","ja":"サイズ"}}],"style":{"add":"btn-success"},"title":"サイズ","title_i18n":{"en":"Size","ja":"サイズ"}},{"add":"New","key":"parentkey[].fileDate","items":[{"key":"parentkey[].fileDate[].fileDateType","type":"select","title":"日付タイプ","titleMap":[{"name":"Accepted","value":"Accepted"},{"name":"Collected","value":"Collected"},{"name":"Copyrighted","value":"Copyrighted"},{"name":"Issued","value":"Issued"},{"name":"Submitted","value":"Submitted"},{"name":"Updated","value":"Updated"},{"name":"Valid","value":"Valid"}],"title_i18n":{"en":"Date Type","ja":"日付タイプ"}},{"key":"parentkey[].fileDate[].fileDateValue","type":"template","title":"日付","format":"yyyy-MM-dd","title_i18n":{"en":"Date","ja":"日付"},"templateUrl":"/static/templates/weko_deposit/datepicker.html"}],"style":{"add":"btn-success"},"title":"日付","title_i18n":{"en":"Date","ja":"日付"}},{"key":"parentkey[].version","type":"text","title":"バージョン情報","title_i18n":{"en":"Version Information","ja":"バージョン情報"}},{"key":"parentkey[].displaytype","type":"select","title":"表示形式","titleMap":[{"name":"詳細表示","value":"detail","name_i18n":{"en":"Detail","ja":"詳細表示"}},{"name":"簡易表示","value":"simple","name_i18n":{"en":"Simple","ja":"簡易表示"}},{"name":"プレビュー","value":"preview","name_i18n":{"en":"Preview","ja":"プレビュー"}}],"title_i18n":{"en":"Preview","ja":"表示形式"}},{"key":"parentkey[].licensetype","type":"select","title":"ライセンス","titleMap":[],"title_i18n":{"en":"License","ja":"ライセンス"}},{"key":"parentkey[].licensefree","type":"textarea","title":" ","condition":"model.parentkey[arrayIndex].licensetype == ''license_free''"},{"key":"parentkey[].accessrole","type":"radios","title":"アクセス","default":"open_restricted","titleMap":[{"name":"オープンアクセス","value":"open_access","name_i18n":{"en":"Open Access","ja":"オープンアクセス"}},{"name":"オープンアクセス日を指定する","value":"open_date","name_i18n":{"en":"Input Open Access Date","ja":"オープンアクセス日を指定する"}},{"name":"ログインユーザのみ","value":"open_login","name_i18n":{"en":"Registered User Only","ja":"ログインユーザのみ"}},{"name":"公開しない","value":"open_no","name_i18n":{"en":"Do Not Publish","ja":"公開しない"}},{"name":"制限公開","value":"open_restricted","name_i18n":{"en":"Limited Access","ja":"制限公開"}}],"title_i18n":{"en":"Access","ja":"アクセス"}},{"key":"parentkey[].accessdate","type":"template","title":"公開日","format":"yyyy-MM-dd","condition":"model.parentkey[arrayIndex].accessrole == ''open_date''","title_i18n":{"en":"Opendate","ja":"公開日"},"templateUrl":"/static/templates/weko_deposit/datepicker.html"},{"key":"parentkey[].dataType","type":"select","title":"データタイプ","titleMap":[{"name":"Life","value":"life","name_i18n":{"en":"Life","ja":"ライフ"}},{"name":"Accumulation","value":"accumulation","name_i18n":{"en":"Accumulation","ja":"累積"}},{"name":"Combinational Analysis","value":"combinational_analysis","name_i18n":{"en":"Combinational Analysis","ja":"組合せ分析"}},{"name":"Perfectures","value":"perfectures","name_i18n":{"en":"Perfectures","ja":"都道府県"}},{"name":"Location Information","value":"location_information","name_i18n":{"en":"Location Information","ja":"地点情報"}}],"condition":"model.parentkey[arrayIndex].accessrole == ''open_restricted''","title_i18n":{"en":"Data Type","ja":"データタイプ"}},{"add":"New","key":"parentkey[].provide","items":[{"key":"parentkey[].provide[].workflow","type":"select","title":"ワークフロー","titleMap":[],"title_i18n":{"en":"WorkFlow","ja":"ワークフロー"}},{"key":"parentkey[].provide[].role","type":"select","title":"ロール","titleMap":[],"title_i18n":{"en":"Role","ja":"ロール"}}],"style":{"add":"btn-success"},"title":"提供方法","condition":"model.parentkey[arrayIndex].accessrole == ''open_restricted''","title_i18n":{"en":"Providing Method","ja":"提供方法"}},{"key":"parentkey[].terms","type":"select","title":"利用規約","titleMap":[],"condition":"model.parentkey[arrayIndex].accessrole == ''open_restricted''","title_i18n":{"en":"Terms and Conditions","ja":"利用規約"}},{"key":"parentkey[].termsDescription","type":"textarea","title":" ","condition":"model.parentkey[arrayIndex].accessrole == ''open_restricted'' && model.parentkey[arrayIndex].terms== ''term_free''"},{"key":"parentkey[].billing","type":"template","templateUrl":"/static/templates/weko_deposit/checkboxes.html","condition":"model.parentkey[arrayIndex].accessrole == ''open_date'' || model.parentkey[arrayIndex].accessrole == ''open_login''","title":"課金","titleMap":[{"value":"billing_file","name":"課金ファイル","name_i18n":{"en":"Billing file","ja":"課金ファイル"}}],"title_i18n":{"en":"Billing","ja":"課金"}},{"key":"parentkey[].role","add":"New","style":{"add":"btn-success"},"condition":"model.parentkey[arrayIndex].accessrole == ''open_login'' && model.parentkey[arrayIndex].billing != ''billing_file''","title":"ロール","items":[{"key":"parentkey[].role[].role","type":"select","title":"ロール","titleMap":[],"title_i18n":{"en":"Role","ja":"ロール"}}],"title_i18n":{"en":"Role","ja":"ロール"}},{"key":"parentkey[].priceinfo","add":"New","style":{"add":"btn-success"},"condition":"(model.parentkey[arrayIndex].accessrole == ''open_date'' || model.parentkey[arrayIndex].accessrole == ''open_login'') && model.parentkey[arrayIndex].billing == ''billing_file''","title":"価格情報","items":[{"key":"parentkey[].priceinfo[].billingrole","type":"select","title":"ロール","titleMap":[],"title_i18n":{"en":"Role","ja":"ロール"}},{"key":"parentkey[].priceinfo[].tax","type":"template","templateUrl":"/static/templates/weko_deposit/checkboxes.html","title":"税","titleMap":[{"value":"include_tax","name":"税込","name_i18n":{"en":"Include tax","ja":"税込"}}],"title_i18n":{"en":"Tax","ja":"税"}},{"key":"parentkey[].priceinfo[].price","type":"text","title":"価格","title_i18n":{"en":"Price","ja":"価格"}}],"title_i18n":{"en":"Price","ja":"価格情報"}}],"style":{"add":"btn-success"},"title_i18n":{"en":"Restricted Access Content File","ja":"制限公開用のコンテンツファイル"}}',
        false,
        null
    );

insert into
    admin_settings (id, name, settings)
values
    (
        (select max(id) + 1 from admin_settings),
        'billing_settings',
        '{"currency_unit":"&yen;","tax_rate":0.1}'
    ),
    (
        (select max(id) + 2 from admin_settings),
        'repository_charge_settings',
        '{"protocol":"https","fqdn":"","user":"","password":"","sys_id":""}'
    ),
    (
        (select max(id) + 3 from admin_settings),
        'proxy_settings',
        '{"use_proxy":false,"host":"","port":"","user":"","password":""}'
    );
