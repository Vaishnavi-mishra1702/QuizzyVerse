<template>
  <div class="container my-5">
    <div class="d-flex justify-content-between align-items-center mb-3">
      <h2 class="text-success">Excited for the Challenge!!</h2>
      <h5 class="text-danger">⏳ Time Left: {{ formattedTime }}</h5>
    </div>

    <div v-if="questions.length">
      <div
        v-for="(question, index) in questions"
        :key="question.id"
        class="card mb-4 shadow-sm"
      >
        <div class="card-body">
          <h5 class="card-title">Q{{ index + 1 }}: {{ question.text }}</h5>
          <div class="form-check" v-for="(option, idx) in question.options" :key="idx">
            <input
              class="form-check-input"
              type="radio"
              :name="'question-' + question.id"
              :value="option"
              v-model="userAnswers[question.id]"
            />
            <label class="form-check-label">{{ option }}</label>
          </div>
        </div>
      </div>

      <div class="text-center mt-4">
        <button class="btn btn-secondary me-2" @click="cancelQuiz">Cancel</button>
        <button class="btn btn-primary" @click="submitQuiz">Submit</button>
      </div>
    </div>

    <div v-else class="text-center text-muted mt-5">
      <p>Loading quiz questions...</p>
    </div>
  </div>
</template>

<script>
import axios from "axios";

export default {
  data() {
    return {
      quizId: this.$route.params.id,
      questions: [],
      userAnswers: {},
      duration: 0, // in minutes
      timeLeft: 0, // in seconds
      timerInterval: null,
    };
  },
  computed: {
    formattedTime() {
      const minutes = Math.floor(this.timeLeft / 60)
        .toString()
        .padStart(2, "0");
      const seconds = (this.timeLeft % 60).toString().padStart(2, "0");
      return `${minutes}:${seconds}`;
    },
  },
  async mounted() {
    await this.fetchQuizQuestions();
    this.startTimer();
  },
  beforeUnmount() {
    clearInterval(this.timerInterval);
  },
  methods: {
    async fetchQuizQuestions() {
      try {
        const token = localStorage.getItem("token");
        const headers = { Authorization: `Bearer ${token}` };
        const res = await axios.get(
          `http://127.0.0.1:5000/api/user/quizzes/${this.quizId}/questions`,
          { headers }
        );
        this.questions = res.data.questions;
        this.duration = res.data.duration; // fetched from backend in minutes

        this.timeLeft = this.duration * 60; // convert to seconds

        // Initialize userAnswers
        this.questions.forEach((q) => {
          this.userAnswers[q.id] = "";
        });
      } catch (error) {
        console.error("Failed to load questions", error);
      }
    },

    startTimer() {
      this.timerInterval = setInterval(() => {
        if (this.timeLeft > 0) {
          this.timeLeft--;
        } else {
          clearInterval(this.timerInterval);
          alert("⏰ Time's up! Auto-submitting the quiz.");
          this.submitQuiz();
        }
      }, 1000);
    },

    async submitQuiz() {
      clearInterval(this.timerInterval);

      let score = 0;
      this.questions.forEach((q) => {
        if (this.userAnswers[q.id] === q.correct_option) {
          score += 1;
        }
      });

      try {
        const token = localStorage.getItem("token");
        const headers = { Authorization: `Bearer ${token}` };

        await axios.post(
          "http://127.0.0.1:5000/api/quiz/submit",
          {
            quiz_id: this.quizId,
            answers: this.userAnswers,
            score: score,
          },
          { headers }
        );

        alert(`✅ Quiz submitted! Your score is ${score} / ${this.questions.length}`);
        this.$router.push("/userdashboard");
      } catch (error) {
        console.error("Error submitting quiz", error);
        alert("❌ Something went wrong while submitting the quiz.");
      }
    },

    cancelQuiz() {
      if (confirm("Are you sure you want to cancel the quiz? Your progress will be lost.")) {
        clearInterval(this.timerInterval);
        this.$router.push("/userdashboard");
      }
    },
  },
};
</script>

<style scoped>
.card {
  border-radius: 10px;
}
.card-title {
  font-weight: bold;
}
</style>
