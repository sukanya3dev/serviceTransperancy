new Vue({
  el: '#app',
  data: {
    owner: '',
    landId: '',
    location: '',
    message: ''
  },
  methods: {
    async submitForm() {
      const data = {
        owner: this.owner,
        landId: this.landId,
        location: this.location
      };
      const result = await postData('register', data);
      this.message = result.message || 'Registration successful!';
    }
  }
});
