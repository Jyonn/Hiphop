class Method {
    static staticConstructor() {
        this.GET = 'get';
        this.POST = 'post';
        this.PUT = 'put';
        this.DELETE = 'delete';
    }
}

class ErrorHandler {
    static handler(error) {
        console.error(error);
        // return Promise.reject(error);
    }
}

class Request {
    static staticConstructor() {
        this._handler = null;
    }

    static getQueryString(params) {
      const esc = encodeURIComponent;
      return Object.keys(params)
        .map(k => esc(k) + '=' + esc(params[k]))
        .join('&');
    }

    static async baseFetch(method, url, data=null, credential=true, json=true) {
        if ((method === Method.GET || method === Method.DELETE) && data) {
            url += '?' + this.getQueryString(data);
            data = null;
        }
        let credentials = credential ? "include" : 'omit';
        let req;
        if (json) {
            req = await fetch(url, {
                method: method,
                headers: {
                    "Content-type": "application/json",
                },
                body: data ? JSON.stringify(data) : null,
                credentials: credentials,
            });
        } else {
            req = await fetch(url, {
                method: method,
                body: data,
                credentials: credentials,
            });
        }
        return req.json().then((resp) => {
            if (resp.code !== 0) {
                if (!this._handler || this._handler(resp)) {
                    alert(resp.msg);
                }
                return ErrorHandler.handler(resp);
            }
            return resp.body;
        }).catch(ErrorHandler.handler);
    }
    static async get(url, data=null, credential=true, json=true) {
        return this.baseFetch(Method.GET, url, data, credential, json);
    }
    static async post(url, data=null, credential=true, json=true) {
        return this.baseFetch(Method.POST, url, data, credential, json);
    }
    static async put(url, data=null, credential=true, json=true) {
        return this.baseFetch(Method.PUT, url, data, credential, json);
    }
    static async delete(url, data=null, credential=true, json=true) {
        return this.baseFetch(Method.DELETE, url, data, credential, json);
    }
}

Method.staticConstructor();
Request.staticConstructor();
