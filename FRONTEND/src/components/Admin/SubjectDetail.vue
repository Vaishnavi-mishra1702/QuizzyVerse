<template>
  <div class="container mt-5">
    <h2 class="mb-4 text-primary">Subject Details</h2>
    <div v-if="subject">
      <p><strong>Name:</strong> {{ subject.name }}</p>
      <p><strong>Description:</strong> {{ subject.description }}</p>
    </div>
    <div v-else>
      <p>Loading subject details...</p>
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  data() {
    return {
      subject: null
    }
  },
  mounted() {
    const id = this.$route.params.id
    const token = localStorage.getItem('token')

    axios.get(`http://127.0.0.1:5000/api/subjects/${id}`, {
      headers: { Authorization: `Bearer ${token}` }
    })
    .then(res => {
      this.subject = res.data
    })
    .catch(err => {
      console.error('Error fetching subject:', err)
    })
  }
}
</script>
