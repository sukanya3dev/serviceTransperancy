new Vue({
  el: '#app',
  data: {
    name: '',
    feedback: '',
    message: ''
  },
  methods: {
    async submitFeedback() {
      const data = {
        name: this.name,
        feedback: this.feedback
      };
      const result = await postData('feedback', data);
      this.message = result.message || 'Feedback submitted!';
    }
  }
});
