import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

export const constantRouterMap = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/common/Login')
  }
]

export const asyncRouterMap = [
  {
    path: '/',
    redirect: { path: '/home' }
  },
  {
    path: '/home',
    name: 'Home',
    component: () => import('@/views/Home'),
    children: [
      {
        path: 'kanban',
        component: () => import('@/views/workshop/Kanban'),
        meta: {
          role: ['admin', 'super_editor', 'viewer'],
          isSidebarItem: true,
          subsystem: 'workshop',
          sidebarInfo: {
            name: '车间看板',
            iconClass: 'icon-laptop'
          }
        }
      },
      {
        path: 'controlGraph/:proIndex/:parIndex',
        component: () => import('@/views/workshop/ControlGraph'),
        meta: {
          role: ['admin', 'super_editor', 'viewer'],
          isSidebarItem: false,
          subsystem: 'workshop'
        }
      },
      {
        path: 'productManager',
        component: () => import('@/views/workshop/ProductManager'),
        meta: {
          role: ['admin', 'super_editor'],
          isSidebarItem: true,
          subsystem: 'workshop',
          sidebarInfo: {
            name: '零件管理',
            iconClass: 'icon-plus-circle'
          }
        }
      },
      {
        path: 'workshopManager',
        component: () => import('@/views/workshop/WorkshopManager'),
        meta: {
          role: ['admin', 'super_editor'],
          isSidebarItem: true,
          subsystem: 'workshop',
          sidebarInfo: {
            name: '车间管理',
            iconClass: 'icon-archive1'
          }
        }
      },
      {
        path: 'analysisReports',
        component: () => import('@/views/workshop/AnalysisReports'),
        meta: {
          role: ['admin', 'super_editor', 'viewer'],
          isSidebarItem: true,
          subsystem: 'workshop',
          sidebarInfo: {
            name: '异常警报',
            iconClass: 'icon-bell'
          }
        }
      },
      {
        path: 'UserManage',
        component: () => import('@/views/workshop/UserManage'),
        meta: {
          role: ['admin', 'super_editor',],
          isSidebarItem: true,
          subsystem: 'workshop',
          sidebarInfo: {
            name: '用户管理',
            iconClass: 'icon-grid'
          }
        }
      },
      {
        path: 'analysisReportDetail/:index',
        name: 'ReportDetail',
        component: () => import('@/views/workshop/AnalysisReportDetail'),
        meta: {
          role: ['admin', 'super_editor', 'viewer'],
          isSidebarItem: false,
          subsystem: 'workshop'
        }
      },
      {
        path: 'opcuaManage',
        component: () => import('@/views/workshop/OpcuaManage'),
        meta: {
          role: ['admin', 'super_editor', 'viewer'],
          isSidebarItem: true,
          sidebarInfo: {
            name: 'OPC UA',
            iconClass: 'icon-cloud_queue'
          }
        }
      },
      {
        path: 'accountSettings',
        component: () => import('@/views/common/AccountSettings'),
        meta: {
          role: ['admin', 'super_editor', 'viewer'],
          isSidebarItem: true,
          sidebarInfo: {
            name: '账户设置',
            iconClass: 'icon-user1'
          }
        }
      },
      {
        path: '404',
        name: 'Small404',
        component: () => import('@/views/common/Error')
      },
      {
        path: 'welcome',
        name: 'Welcome',
        component: () => import('@/views/common/Welcome')
      }
    ],
    meta: {
      role: ['admin', 'super_editor', 'viewer'],
      isSidebarItem: false
    }
  },
  {
    path: '/404',
    component: () => import('@/views/common/Error')
  },
  { path: '*', redirect: '/404', hidden: true },
]

// Mount constant router map by default
const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes: constantRouterMap
})

export default router
