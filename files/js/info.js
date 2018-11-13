class Info {
    static staticConstructor() {
        this.template = template`
            <div id="${0}" class="${1} inactive">
                <div class="text">${2}</div>
            </div>`;
        this.TYPE_SUCC = 'succ';
        this.TYPE_WARN = 'warn';
        this.TYPE_ERROR = 'error';
        this.TYPE_LIST = [this.TYPE_SUCC, this.TYPE_WARN, this.TYPE_ERROR];

        this.activateTime = 500;
    }

    constructor(text, type=Info.TYPE_ERROR, timeout=0) {
        // timeout 0 自动 / -1 永久 / >0 秒
        this.text = text;
        if (Info.TYPE_LIST.indexOf(type) === -1) {
            this.type = Info.TYPE_ERROR;
        } else {
            this.type = type;
        }
        this.id = get_random_string();
        this.html = stringToHtml(Info.template(this.id, this.type, this.text));
        this.clock = null;
        this.timeout = timeout;
    }

    remove() {
        clearTimeout(this.clock);
        deactivate(this.html);
        setTimeout(() => {
            this.html.remove();
        }, Info.activateTime);
    }

    setClock() {
        if (this.timeout < 0) {
            return;
        }
        let timeout = 500 + this.text.length * 250;
        if (this.timeout > 0) {
            timeout = this.timeout * 1000;
        }
        this.clock = setTimeout(() => {
            this.remove();
        }, timeout);
    }
}

class InfoCenter {
    static staticConstructor(selector) {
        this.infoContainer = document.getElementById(selector);
    }

    static push(info) {
        InfoCenter.infoContainer.appendChild(info.html);
        setTimeout(() => {
            activate(info.html);
        }, Info.activateTime);
        info.setClock();
        info.html.addEventListener("click", () => {
            info.remove();
        });
    }

    static delayInfo(info, callback, timeout = 3000) {
        return function() {
            setTimeout(callback, timeout);
            if (info) {
                InfoCenter.push(info);
            }
        }
    }
}

Info.staticConstructor();
InfoCenter.staticConstructor();
