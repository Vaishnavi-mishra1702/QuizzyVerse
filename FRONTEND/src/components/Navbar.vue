<script setup>
import { ref, onMounted, watchEffect, nextTick } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'

const router = useRouter()

const userType = ref(null)
const searchTerm = ref('')
const allData = ref([])
const filteredResults = ref([])

const logoutUser = () => {
  localStorage.clear()
  userType.value = null
  router.push('/')
}

const getUserType = () => {
  userType.value = localStorage.getItem('userType')
}

const fetchSearchData = async () => {
  try {
    const token = localStorage.getItem('token')
    const headers = { Authorization: `Bearer ${token}` }

    const [users, subjects, quizzes] = await Promise.all([
      axios.get('http://127.0.0.1:5000/admin/users', { headers }),
      axios.get('http://127.0.0.1:5000/api/subjects', { headers }),
      axios.get('http://127.0.0.1:5000/admin/quizzes', { headers })
    ])

    allData.value = [
      ...users.data.map(u => ({
        id: u.id,
        label: u.name || u.username || `User ${u.id}`,
        type: 'User'
      })),
      ...subjects.data.map(s => ({
        id: s.id,
        label: s.name || `Subject ${s.id}`,
        type: 'Subject'
      })),
      ...quizzes.data.map(q => ({
        id: q.id,
        label: `Quiz ${q.id}`,
        type: 'Quiz'
      }))
    ]
  } catch (error) {
    console.error('Error fetching search data:', error)
  }
}

const handleSearch = () => {
  const keyword = searchTerm.value.trim().toLowerCase()
  if (!keyword) {
    filteredResults.value = []
    return
  }

  filteredResults.value = allData.value.filter(item => {
    const label = item.label.toLowerCase()
    const id = String(item.id)
    return label.includes(keyword) || id === keyword
  })
}

const navigateTo = async (item) => {
  searchTerm.value = ''
  filteredResults.value = []

  if (item.type === 'User') {
    router.push(`/admin/users/${item.id}`)
  } else if (item.type === 'Subject') {
    if (router.currentRoute.value.path !== '/dashboard') {
      await router.push('/dashboard')
    }
    await nextTick()
    const el = document.querySelector(`[data-subject-id="${item.id}"]`)
    if (el) {
      el.scrollIntoView({ behavior: 'smooth', block: 'center' })
      el.classList.add('border', 'border-success')
      setTimeout(() => el.classList.remove('border', 'border-success'), 1500)
    }
  } else if (item.type === 'Quiz') {
    if (router.currentRoute.value.path !== '/quiz') {
      await router.push('/quiz')
    }
    await nextTick()
    const el = document.querySelector(`[data-quiz-id="${item.id}"]`)
    if (el) {
      el.scrollIntoView({ behavior: 'smooth', block: 'center' })
      el.classList.add('border', 'border-success')
      setTimeout(() => el.classList.remove('border', 'border-success'), 1500)
    }
  }
}

onMounted(() => {
  getUserType()
})

watchEffect(() => {
  if (userType.value === 'admin') {
    fetchSearchData()
  }
})
</script>

<template>
  <nav class="navbar bg-primary-subtle">
    <div class="container-fluid">
      <RouterLink class="navbar-brand" to="/">QuizzyVerse</RouterLink>

      <div class="d-flex align-items-center flex-wrap gap-2">
        <template v-if="!userType">
          <RouterLink class="btn btn-primary me-2" to="/">Home</RouterLink>
        </template>

        <template v-else-if="userType === 'admin'">
          <RouterLink class="btn btn-secondary me-2" to="/dashboard">Home</RouterLink>
          <RouterLink class="btn btn-secondary me-2" to="/summary">Summary</RouterLink>
          <RouterLink class="btn btn-secondary me-2" to="/quiz">Quiz</RouterLink>

          <!-- 🔍 Search Bar -->
          <div class="position-relative">
            <input
              v-model="searchTerm"
              @input="handleSearch"
              type="text"
              class="form-control"
              placeholder="🔍 Search users, quizzes, subjects..."
              style="width: 250px;"
            />
            <ul
              v-if="filteredResults.length"
              class="list-group position-absolute bg-white shadow mt-1"
              style="z-index: 999; max-height: 200px; overflow-y: auto; width: 100%;"
            >
              <li
                v-for="(item, index) in filteredResults"
                :key="index"
                class="list-group-item list-group-item-action"
                @click="navigateTo(item)"
                style="cursor: pointer;"
              >
                {{ item.type }}: {{ item.label }}
              </li>
            </ul>
          </div>

          <button @click="logoutUser" class="btn btn-danger">Logout</button>
        </template>

        <template v-else-if="userType === 'user'">
          <RouterLink class="btn btn-secondary me-2" to="/userdashboard">Home</RouterLink>
          <RouterLink class="btn btn-secondary me-2" to="/usersummary">Summary</RouterLink>
          <RouterLink class="btn btn-secondary me-2" to="/score">Score</RouterLink>
          <button @click="logoutUser" class="btn btn-danger">Logout</button>
        </template>
      </div>
    </div>
  </nav>
</template>

<style scoped>
.navbar .btn {
  margin-right: 0.5rem;
}
</style>  