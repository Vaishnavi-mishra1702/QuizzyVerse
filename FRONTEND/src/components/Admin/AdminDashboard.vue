<template>
  <div class="container my-5">
    <h2 class="text-primary text-center mb-5">👋 Hello Admin, Welcome to your Dashboard</h2>

    <div v-if="loading" class="text-center">
      <div class="spinner-border text-primary" role="status"></div>
    </div>

    <div v-else class="row g-4">
      <div
        v-for="subject in subjects"
        :key="subject.id"
        class="col-md-6 col-lg-4"
        :data-subject-id="subject.id"

      >

        <div class="card h-100 shadow-sm border-primary">
          <div class="card-header bg-primary text-white text-center fs-5 fw-bold">
            {{ subject.name }}
          </div>
          <div class="card-body">
            <!-- <p class="text-muted">{{ subject.description }}</p> -->

            <div class="mb-3 d-flex justify-content-center gap-2">
              <button @click="editSubject(subject.id)" class="btn btn-sm btn-outline-primary">
                ✏️ Manage Subject
              </button>
              <!-- <button @click="this.$router.push('/manageSubjects')" class="btn btn-sm btn-outline-danger">
                🗑️ Delete Subject
              </button> -->
            </div>

            <hr />

            <div
              v-for="chapter in subject.chapters"
              :key="chapter.id"
              class="mb-3 border-bottom pb-2"
            >
              <h6 class="mb-1">📘 {{ chapter.name }}</h6>
              <!-- <p class="mb-1 text-muted">Questions: {{ chapter.num_questions }}</p> -->
              <button
                @click="editChapter(subject.id, chapter.id)"
                class="btn btn-sm btn-outline-primary me-2"
              >
                Manage Chapter
              </button>
              <!-- <button
                @click="deleteChapter(subject.id, chapter.id)"
                class="btn btn-sm btn-outline-danger"
              >
                Delete
              </button> -->
            </div>

            <button
              @click="goToAddChapter(subject.id)"
              class="btn btn-success w-100 mt-3"
            >
              ➕ Add New Chapter
            </button>
          </div>
        </div>
      </div>
    </div>

    <div class="text-center mt-5">
      <button @click="this.$router.push('/addSubject')" class="btn btn-lg btn-outline-success">
        ➕ Add New Subject
      </button>
    </div>
    <div class="mt-4">
      <h4>🛠 Celery Admin Tasks</h4>

      <button class="btn btn-primary me-2" @click="sendMonthlyReport">📧 Send Monthly Report</button>
      <button class="btn btn-warning me-2" @click="sendDailyReminder">⏰ Daily Reminder</button>
      <button class="btn btn-danger" @click="exportAdminCsv">📊 Export Admin CSV</button>

      <div v-if="taskStatus" class="alert alert-info mt-3">{{ taskStatus }}</div>
      <div v-if="downloadLink" class="mt-2">
        <a :href="downloadLink" class="btn btn-outline-primary" download>⬇️ Download File</a>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import { useRouter } from 'vue-router'
import UserInfo from './UserInfo.vue'
// --------------------------
// 📦 Celery Task State
// --------------------------
const BASE_URL = 'http://127.0.0.1:5000'

const taskStatus = ref('')
const downloadLink = ref('')

const triggerTask = async (path, returnsFile = false) => {
  taskStatus.value = "Starting task..."
  downloadLink.value = ''

  const res = await fetch(`${BASE_URL}${path}`)
  const data = await res.json()

  checkStatus(data.task_id, returnsFile)
}

const sendMonthlyReport = () => {
  triggerTask('/api/send/monthly_report')  // no file
}

const sendDailyReminder = () => {
  triggerTask('/api/send/daily_reminder')  // no file
}

const exportAdminCsv = () => {
  triggerTask('/api/export/admin_csv', true)  // ✅ this returns a file
}

const checkStatus = async (taskId, returnsFile) => {
  const interval = setInterval(async () => {
    const res = await fetch(`${BASE_URL}/api/task_result/${taskId}`)
    const data = await res.json()

    if (data.status === "SUCCESS") {
      clearInterval(interval)
      taskStatus.value = "✅ Task completed."

      if (returnsFile && data.result) {
        downloadLink.value = `${BASE_URL}/static/${data.result}`
      }
    } else if (data.status === "FAILURE") {
      clearInterval(interval)
      taskStatus.value = "❌ Task failed."
    } else {
      taskStatus.value = `⏳ Status: ${data.status}`
    }
  }, 2000)
}


// --------------------------
// 📚 Subject & Chapter Logic
// --------------------------
const subjects = ref([])
const loading = ref(true)
const router = useRouter()

const fetchSubjects = async () => {
  const token = localStorage.getItem('token')

  try {
    const response = await axios.get('http://127.0.0.1:5000/api/subjects', {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
    subjects.value = response.data
  } catch (err) {
    console.error('Failed to fetch subjects:', err)
  } finally {
    loading.value = false
  }
}

const editChapter = (subjectId, chapterId) => {
  router.push(`/edit-chapter/${subjectId}/${chapterId}`)
}

const deleteChapter = async (subjectId, chapterId) => {
  const token = localStorage.getItem('token')
  if (!confirm('Are you sure you want to delete this chapter?')) return

  try {
    await axios.delete(
      `http://127.0.0.1:5000/api/subjects/${subjectId}/chapters/${chapterId}`,
      {
        headers: {
          Authorization: `Bearer ${token}`
        }
      }
    )
    fetchSubjects()
  } catch (err) {
    alert('Error deleting chapter.')
    console.error(err)
  }
}

const goToAddChapter = (subjectId) => {
  router.push(`/add-chapter/${subjectId}`)
}

const goToAddSubject = () => {
  router.push('/add-subject')
}

const editSubject = (subjectId) => {
  router.push(`/edit-subject/${subjectId}`)
}

const deleteSubject = async (subjectId) => {
  const token = localStorage.getItem('token')
  if (!confirm('Are you sure you want to delete this subject?')) return

  try {
    await axios.delete(
      `http://127.0.0.1:5000/api/subjects/${subjectId}`,
      {
        headers: {
          Authorization: `Bearer ${token}`
        }
      }
    )
    fetchSubjects()
  } catch (err) {
    alert('Error deleting subject.')
    console.error(err)
  }
}

onMounted(fetchSubjects)

// 🔍 Optional scroll logic for dynamic search highlighting
// setTimeout(() => {
//   const el = document.querySelector(`[ref="subject-${item.id}"]`)
//   if (el) {
//     el.scrollIntoView({ behavior: 'smooth', block: 'center' })
//     el.classList.add('border', 'border-success')
//     setTimeout(() => el.classList.remove('border', 'border-success'), 1500)
//   }
// }, 300)
</script>

<style scoped>
.card-header {
  font-size: 1.25rem;
  background: linear-gradient(135deg, #1e90ff, #00bfff);
  color: white;
  border-radius: 0.5rem 0.5rem 0 0;
}
.card-body {
  background-color: #f9f9f9;
}
.card {
  border-radius: 1rem;
  transition: transform 0.2s ease-in-out;
}
.card:hover {
  transform: scale(1.02);
}
.border-success {
  box-shadow: 0 0 10px 3px #28a74599;
  transition: box-shadow 0.3s ease;
}

</style>
