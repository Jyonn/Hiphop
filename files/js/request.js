function request(url, method, data, callback) {
    fetch(url,
        {
            credentials: 'include',
            method: method,
            headers: {
                "Accept": "application/json",
                "Content-Type": "application/json"
            },
            body: (data === null) ? null : JSON.stringify(data),
        })
        .then((response) => {
            if (response.status === 200)
                return response;
        })
        .then((data) => {
            return data.json();
        })
        .then((data) => {
            callback(data);
        })
        .catch((err) => console.log(err))
}
