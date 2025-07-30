import { createWebHistory, createRouter } from "vue-router"

// General components
import Content from "./components/Content.vue"
import LoginPage from "./components/LoginPage.vue"
import RegisterPage from "./components/RegisterPage.vue"

// Admin Components
import AdminDashboard from "./components/Admin/AdminDashboard.vue"
import AddChapter from "./components/Admin/AddChapter.vue"
import AddSubject from "./components/Admin/AddSubject.vue"
import AddQuiz from "./components/Admin/AddQuiz.vue"
import AddQuestion from "./components/Admin/AddQuestion.vue"
import Quizzes from "./components/Admin/Quizes.vue"
import ManageChapters from "./components/Admin/ManageChapters.vue"
import ManageQuiz from "./components/Admin/ManageQuiz.vue"
import ManageQuestions from "./components/Admin/ManageQuestions.vue"
import ViewQuestions from "./components/Admin/ViewQuestions.vue"
import SummaryCharts from "./components/Admin/SummaryCharts.vue"
import UserSummary from "./components/Users/UserSummary.vue"
import EditSubject from "./components/Admin/EditSubject.vue"

// Optional future components
// import RequestCard from "./components/RequestCardManageSubjects.vue"
import UserDashboard from "./components/Users/UserDashboard.vue"
import  StartQuiz from "./components/Users/StartQuiz.vue"
import  Score from "./components/Users/Score.vue"
const routes = [
  // General routes
  { path: "/", component: Content },
  { path: "/login", component: LoginPage },
  { path: "/register", component: RegisterPage },

  // Admin Dashboard
  { path: "/dashboard", component: AdminDashboard },
  { path: "/userdashboard", component: UserDashboard },
  { path: "/score", component: Score },
  { path: "/quiz/start/:id",component: StartQuiz, props: true },
  // Quiz Management
  { path: "/quiz", component: Quizzes },
  { path: "/add-quiz/:chapterId", component: AddQuiz, props: true },
  { path: "/add-question/:quizId?", component: AddQuestion, props: true },
  { path: "/view-questions/:quizId", component: ViewQuestions, props: true },
  { path: "/manage-quiz/:quizId", component: ManageQuiz, props: true },
  {
    path: "/manage-questions/:questionId/:quizId",
    name: "ManageQuestions",
    component: ManageQuestions,
    props: true,
  },

  // Subject and Chapter
  { path: "/addSubject", component: AddSubject },
  { path: "/add-chapter/:subjectId", component: AddChapter, props: true },
  { path: "/edit-subject/:subjectId", component: EditSubject, props: true },
  { path: "/edit-chapter/:subjectId/:chapterId", component: ManageChapters, props: true },

  // Summary Charts
  {
    path: "/summary",
    name: "SummaryCharts",
    component: SummaryCharts,
  },
{
    path: "/usersummary",
    name: "UserSummary",
    component: UserSummary,
  },

  // 👉 Search result redirection routes
  {
    path: "/admin/users/:id",
    name: "UserInfo",
    component: () => import("./components/Admin/UserInfo.vue"), // Create this
    props: true,
  },
  {
    path: "/admin/subjects/:id",
    name: "SubjectDetail",
    component: () => import("./components/Admin/SubjectDetail.vue"), // Create this
    props: true,
  },
  {
    path: "/admin/quizzes/:id",
    name: "QuizDetail",
    component: () => import("./components/Admin/QuizDetail.vue"), // Create this
    props: true,
  }

  // Future:
  // { path: "/user/request/:cardname", component: RequestCard }
]

export const router = createRouter({
  history: createWebHistory(),
  routes
})
router.beforeEach((to, from, next) => {
  const isAuthenticated = !!localStorage.getItem('token')
  const userRole = localStorage.getItem('userType') // 'admin' or 'user'

  if (to.meta.requiresAuth && !isAuthenticated) {
    next('/login') // Redirect to login if not logged in
  } else if (to.meta.allowedRoles && !to.meta.allowedRoles.includes(userRole)) {
    next('/unauthorized') // Redirect if role not allowed
  } else {
    next() // All good, allow navigation
  }
})