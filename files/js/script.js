$(document).ready(function () {
    let results = [];
    let result_container = $('#result');
    let translate = "零单二三四五六七八九十";

    $('button').on('click', function () {
        let input = $('#kw').val(),
            min_max_match = $('#min_max_match').val(),
            phrase_len = $('#phrase_len').val();
        if (!input)
            input = "xie4 chun1 hua1";
        if (!min_max_match || min_max_match < 0)
            min_max_match = 0;
        if (!phrase_len || phrase_len < 0)
            phrase_len = 0;
        let url = `/match?phrase=${input}&min_max_match=${min_max_match}&phrase_len=${phrase_len}&cluster=NORMAL&cluster_type=DEFAULT`;

        url = encodeURI(url);
        request(url, 'GET', null, function (response) {
            let data = response.body;
            results = [];
            for (let item in data) {
                results[parseInt(item)] = data[item];
            }
            result_container.empty();
            for (let i = 10; i > 0; i--) {
                if (!results[i])
                    continue;
                let sub_title = translate[i] + '押';
                let str = '';
                for (let p = 0; p < results[i].length; p++)
                    str += results[i][p] + `&nbsp;`;
                let html = `<div class="result-box"><h3>${sub_title}</h3><p>${str}</p></div>`;
                result_container.append(html);
            }
        });
    })
});