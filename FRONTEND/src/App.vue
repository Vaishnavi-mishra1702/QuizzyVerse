<script setup>
import Content from './components/Content.vue'
import Navbar from './components/Navbar.vue'
import Footer from './components/Footer.vue'
</script>

<template>
  <div>
    <Navbar />
    <RouterView />
    <!-- <Content /> -->
    <Footer />
  </div>
  <!-- <HelloWorld msg="Vite + Vue" /> -->
</template>

