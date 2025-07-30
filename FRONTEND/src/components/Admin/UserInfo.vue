<!-- src/components/Admin/UserInfo.vue -->
<script setup>
import { ref, onMounted, watch } from 'vue'
import axios from 'axios'
import { useRoute } from 'vue-router'

const route = useRoute()

const user = ref(null)
const loading = ref(true)
const error = ref(null)

const fetchUser = async (id) => {
  loading.value = true
  error.value = null
  const token = localStorage.getItem('token')
  try {
    const res = await axios.get(`http://127.0.0.1:5000/api/users/${id}`, {
      headers: {
        Authorization: `Bearer ${token}`
      }
    })
    user.value = res.data
  } catch (err) {
    error.value = 'Failed to load user'
    console.error(err)
  } finally {
    loading.value = false
  }
}

// Run once when component mounts
onMounted(() => {
  fetchUser(route.params.id)
})

// Re-run when route param (id) changes
watch(() => route.params.id, (newId) => {
  fetchUser(newId)
})
</script>

<template>
  <div class="container my-4">
    <h2 class="text-primary mb-3">User Info</h2>

    <p v-if="loading">Loading user...</p>
    <p v-else-if="error">{{ error }}</p>
    <div v-else>
      <table class="table table-bordered table-striped">
        <tbody>
          <tr>
            <th>ID</th>
            <td>{{ user.id }}</td>
          </tr>
          <tr>
            <th>Name</th>
            <td>{{ user.name }}</td>
          </tr>
          <tr>
            <th>Email</th>
            <td>{{ user.email }}</td>
          </tr>
          <tr>
            <th>Role</th>
            <td>{{ user.role }}</td>
          </tr>
        </tbody>
      </table>
    </div>
  </div>
</template>
