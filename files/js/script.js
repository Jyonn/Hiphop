$(document).ready(function () {
    let results = [];
    let result_container = $('#result');
    let translate = "零单二三四五六七八九十";

    $('button').on('click', function () {
        let input = $('input').val();
        if (!input)
            input = "xie4 chun1 hua1";
        let url = `/match?phrase=${input}&min_max_match=0&phrase_len=0`;

        url = encodeURI(url);
        request(url, 'GET', null, function (response) {
            let data = response.body;
            for (let item in data) {
                results[parseInt(item)] = data[item];
            }
            console.log(results);
            result_container.empty();
            for (let i = 10; i > 0; i--) {
                if (!results[i])
                    continue;
                let sub_title = translate[i] + '压';
                let str = '';
                for (let p = 0; p < results[i].length; p++)
                    str += results[i][p] + `&nbsp;`;
                let html = `<div class="result-box"><h3>${sub_title}</h3><p>${str}</p></div>`;
                result_container.append(html);
            }
        });
    })
});