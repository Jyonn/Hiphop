class MainComponent {
    constructor() {
        this.button = document.getElementById('search')
        this.result = document.getElementById('result')
        this.keyword = document.getElementById('kw')
        this.match = document.getElementById('min_max_match')
        this.length = document.getElementById('phrase_len')

        this.translate = "零单二三四五六七八九十";

        this.button.addEventListener('click', this.search.bind(this))

        this.initSelector()
    }

    initSelector() {
        let optionT = template`<option value="${0}">${1}</option>`
        let options = ["不限", "单", "二", "三", "四", "五", "六", "七", "八", "九", "十"]

        let html = ''
        for (let i = 0; i < options.length; i++) {
            html += optionT(i, options[i])
        }
        this.match.innerHTML = html
        this.length.innerHTML = html
    }

    search() {
        let keyword = this.keyword.value
        let match = this.match.value
        let length = this.length.value

        let phraseT = template`<div>${0}</div>`
        let matchT = template`<div class="result-box"><div class="match-title">${0}</div><div class="match-result">${1}</div></div>`

        if (!keyword)
            keyword = "xie4 chun1 hua1";
        if (!match || match < 0)
            match = 0;
        if (!length || length < 0)
            length = 0;

        Request.get('/match', {
            phrase: keyword,
            min_max_match: match,
            phrase_len: length,
            cluster: 'NORMAL',
            cluster_type: 'DEFAULT',
        }).then(resp => {
            this.result.innerHTML = ''

            let results = []
            let empty = true

            for (let item in resp) {
                results[parseInt(item)] = resp[item]
            }

            for (let i = 10; i > 0; i--) {
                if (!results[i])
                    continue;
                empty = false
                let matchTitle = this.translate[i] + '押'
                let matchResult = ''
                for (let phrase of results[i]) {
                    matchResult += phraseT(phrase)
                }
                let matchHtml = matchT(matchTitle, matchResult)
                this.result.appendChild(stringToHtml(matchHtml))
            }

            if (empty) {
                let html = matchT('没有匹配结果', '')
                this.result.appendChild(stringToHtml(html))
            }
        })
    }
}