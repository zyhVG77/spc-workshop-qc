import Vue from 'vue'
import VueRouter from 'vue-router'

Vue.use(VueRouter)

export const constantRouterMap = [
  {
    path: '/login',
    name: 'Login',
    component: () => import('@/views/common/Login')
  },
  {
    path: '/test',
    name: 'Test',
    component: () => import('@/views/warehouse/ControlGraph')
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
        path: 'kanban',
        name: 'Kanban',
        component: () => import('@/views/warehouse/Kanban'),
        meta: {
          role: ['admin', 'warehouse_keeper'],
          isSidebarItem: true,
          subsystem: 'warehouse',
          sidebarInfo: {
            name: '仓库看板',
            iconClass: 'icon-laptop_windows'
          }
        }
      },
      {
        path: 'storageCellGraph',
        component: () => import('@/views/warehouse/StorageCells'),
        meta: {
          role: ['admin', 'warehouse_keeper'],
          isSidebarItem: true,
          subsystem: 'warehouse',
          sidebarInfo: {
            name: '储位管理',
            iconClass: 'icon-layers'
          }
        }
      },
      {
        path: 'PutInForm',
        component: () => import('@/views/warehouse/PutInForm'),
        meta: {
          role: ['admin', 'super_editor', 'viewer'],
          isSidebarItem: true,
          subsystem: 'warehouse',
          sidebarInfo: {
            name: '填写入库单',
            iconClass: 'icon-check'
          }
        }
      },
      {
        path: 'TakeOutForm',
        component: () => import('@/views/warehouse/TakeOutForm'),
        meta: {
          role: ['admin', 'super_editor', 'viewer'],
          isSidebarItem: true,
          subsystem: 'warehouse',
          sidebarInfo: {
            name: '填写出库单',
            iconClass: 'icon-local_shipping'
          }
        }
      },
      {
        path: 'warehouseProductManager',
        name: 'WarehouseProductManager',
        component: () => import('@/views/warehouse/ProductManager'),
        meta: {
          role: ['admin', 'warehouse_keeper'],
          isSidebarItem: true,
          subsystem: 'warehouse',
          sidebarInfo: {
            name: '零件管理',
            iconClass: 'icon-camera1'
          }
        }
      },
      {
        path: 'measureSchedule',
        name: 'measureSchedule',
        component: () => import('@/views/warehouse/MeasureSchedule'),
        meta: {
          role: ['admin', 'warehouse_keeper'],
          isSidebarItem: true,
          subsystem: 'warehouse',
          sidebarInfo: {
            name: '测量计划管理',
            iconClass: 'icon-pencil'
          }
        }
      },
      {
        path: 'controlGraphWarehouse',
        name: 'ControlGraphWarehouse',
        component: () => import('@/views/warehouse/ControlGraph'),
        meta: {
          role: ['admin', 'warehouse_keeper'],
          isSidebarItem: true,
          subsystem: 'warehouse',
          sidebarInfo: {
            name: '质量控制',
            iconClass: 'icon-flash_auto'
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
