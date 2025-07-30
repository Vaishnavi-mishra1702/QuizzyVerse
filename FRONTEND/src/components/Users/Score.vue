<template>
  <div class="container my-5">
    <h2 class="text-primary text-center mb-4">📊 Your Quiz Scores</h2>

    <div v-if="loading" class="text-center">
      <div class="spinner-border text-primary" role="status"></div>
    </div>

    <div v-else-if="quizzes.length" class="row mt-3 g-4">
      <div v-for="(quiz, index) in quizzes" :key="index + '-' + quiz.id" class="col-md-6">
        <div class="card shadow-sm">
          <div class="card-body">
            <h5 class="card-title">Quiz #{{ quiz.id }}</h5>
            <p class="card-text"><strong>Subject:</strong> {{ quiz.subject }}</p>
            <p class="card-text"><strong>Chapter:</strong> {{ quiz.chapter }}</p>
            <p class="card-text"><strong>Duration:</strong> {{ quiz.duration }} minutes</p>
            <p class="card-text"><strong>Date:</strong> {{ quiz.date }}</p>
            <p class="card-text text-success"><strong>Score:</strong> {{ quiz.score }}/{{ quiz.total }}</p>
            <p class="card-text text-info"><strong>Percentage:</strong> {{ quiz.percentage }}%</p>
            <p class="card-text text-muted"><strong>Submitted At:</strong> {{ quiz.submitted_at }}</p>

            <!-- <div class="d-flex justify-content-end gap-2">
              <button class="btn btn-primary" @click="startQuiz(quiz.id)">Start Again</button>
            </div> -->
          </div>
        </div>
      </div>
    </div>

    <div v-else class="text-center text-muted">
      No quiz attempts found.
    </div>
  </div>
</template>

<script>
import axios from 'axios'

export default {
  name: "ScoreView",
  data() {
    return {
      quizzes: [],
      loading: true,
    }
  },
  methods: {
    async fetchScores() {
      try {
        const token = localStorage.getItem("token")
        const res = await axios.get("http://localhost:5000/user/scores", {
          headers: {
            Authorization: `Bearer ${token}`,
          },
        })
        this.quizzes = res.data
      } catch (error) {
        console.error("Error fetching scores:", error)
      } finally {
        this.loading = false
      }
    },
    // startQuiz(quizId) {
    //   this.$router.push(`/user/quiz/${quizId}`)
    // },
  },
  mounted() {
    this.fetchScores()
  },
}
</script>

<style scoped>
.card {
  border-left: 5px solid #0d6efd;
}
</style>
