function getCSRFToken() {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            if (cookie.substring(0, 10) == ('csrftoken' + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(10));
                break;
            }
        }
    }
    return cookieValue;
}
new Vue({
    el: '#wrapper',
    delimiters: ['${', '}'],
    data: {
        loading: false,
        exUser: {'password': null, 'email': null},
        rememberMe: false,
        response: null,
        timeoutLogin: 3,
        loginSuccess: false,
        message: 'xin chao',
    },
    methods: {
        login: function () {
            this.loading = true;
            this.$http.post('/api/v1/jwt/create/', this.exUser)
                .then((response) => {
                    let data = response.body;
                    this.loading = false;
                    this.loginSuccess = true;
                    this.exUser = {'password': null, 'email': null};
                    this.response = response;
                    localStorage.setItem('user-access-token', data.body.access);
                    localStorage.setItem('user-refresh-token', data.body.refresh);
                    setInterval(() => {
                        this.timeoutLogin--;
                    }, 1000);
                    setTimeout(() => {
                        window.location.href = '/'
                    }, 3000);
                })
                .catch((err) => {
                    this.loading = false;
                    console.log(err);
                })
        }

    }
});
