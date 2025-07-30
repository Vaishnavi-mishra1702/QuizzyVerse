<template>
  <div class="container mt-5">
    <h2 class="mb-4 text-primary">Quiz Details</h2>
    <div v-if="quiz">
      <p><strong>ID:</strong> {{ quiz.id }}</p>
      <p><strong>Title:</strong> {{ quiz.title }}</p>
      <p><strong>Description:</strong> {{ quiz.description }}</p>
    </div>
    <div v-else>
      <p>Loading quiz details...</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      quiz: null
    }
  },
  mounted() {
    const id = this.$route.params.id
    const token = localStorage.getItem('token')

    axios.get(`http://127.0.0.1:5000/admin/quizzes/${id}`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    .then(res => {
      this.quiz = res.data
    })
    .catch(err => {
      console.error('Error fetching quiz:', err)
    })
  }
}
</script>
