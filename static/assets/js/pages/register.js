Vue.http.headers.common['X-CSRFToken'] = "{{ csrf_token }}";

new Vue({
    el: '#wrapper',
    delimiters: ['${', '}'],
    data: {
        loading: false,
        exUser: {'username': null, 'password': null, 'email': null},
        termChecked: false,
        errors: [],
        registerSuccess: false,
    },
    mounted: function () {
    },
    methods: {
        register: function () {
            let errors = this.validateData();
            if (errors.length) {

            } else {
                this.loading = true;
                this.$http.post('/auth/users/', this.exUser)
                    .then((response) => {
                        this.loading = false;
                        this.registerSuccess = true;
                        this.exUser = {'username': null, 'password': null, 'email': null};
                        this.termChecked = false;
                    })
                    .catch((err) => {
                        this.loading = false;
                        console.log(err);
                    })
            }
        },
        validateData: function () {
            let errors = [];
            return errors;
        },
    }
});
