<template>
  <div class="container my-5">
    <h2 class="text-center text-primary mb-4">📊 Quiz & Question Statistics</h2>

    <div v-if="loading" class="text-center">
      <div class="spinner-border text-primary" role="status"></div>
    </div>

    <div v-else class="row g-4">
      <div class="col-md-6">
        <h5 class="text-center">Questions per Subject</h5>
        <Bar :data="barChartData" :options="barChartOptions" />
      </div>

      <div class="col-md-6">
        <h5 class="text-center">Quizzes Attempted per Month</h5>
        <Pie :data="pieChartData" :options="pieChartOptions" />
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { Bar, Pie } from 'vue-chartjs'
import {
  Chart as ChartJS, Title, Tooltip, Legend, BarElement,
  ArcElement, CategoryScale, LinearScale
} from 'chart.js'
import axios from 'axios'

ChartJS.register(
  Title, Tooltip, Legend,
  BarElement, ArcElement,
  CategoryScale, LinearScale
)

const loading = ref(true)
const barChartData = ref({})
const pieChartData = ref({})

const barChartOptions = {
  responsive: true,
  plugins: {
    legend: { display: false },
    title: { display: true, text: 'Number of Questions by Subject' }
  }
}

const pieChartOptions = {
  responsive: true,
  plugins: {
    legend: { position: 'bottom' },
    title: { display: true, text: 'Quizzes Attempted by Month' }
  }
}

const fetchChartData = async () => {
  try {
    const token = localStorage.getItem('token')
    const response = await axios.get('http://127.0.0.1:5000/admin/question-quiz-stats', {
      headers: { Authorization: `Bearer ${token}` }
    })

    const barSubjects = response.data.question_bar_chart.map(item => item.subject)
    const barCounts = response.data.question_bar_chart.map(item => item.question_count)

    barChartData.value = {
      labels: barSubjects,
      datasets: [{
        label: 'Questions',
        backgroundColor: '#007bff',
        data: barCounts
      }]
    }

    const pieLabels = response.data.quiz_pie_chart.map(item => item.month)
    const pieData = response.data.quiz_pie_chart.map(item => item.count)

    pieChartData.value = {
      labels: pieLabels,
      datasets: [{
        label: 'Quiz Attempts',
        backgroundColor: ['#007bff', '#28a745', '#ffc107', '#dc3545', '#6f42c1', '#20c997'],
        data: pieData
      }]
    }
  } catch (err) {
    console.error('Error fetching chart data:', err)
  } finally {
    loading.value = false
  }
}

onMounted(fetchChartData)
</script>

<style scoped>
.container {
  max-width: 1000px;
}
</style>
