import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

/* Layout */
import Layout from '@/layout'

/**
 * Note: sub-menu only appear when route children.length >= 1
 * Detail see: https://panjiachen.github.io/vue-element-admin-site/guide/essentials/router-and-nav.html
 *
 * hidden: true                   if set true, item will not show in the sidebar(default is false)
 * alwaysShow: true               if set true, will always show the root menu
 *                                if not set alwaysShow, when item has more than one children route,
 *                                it will becomes nested mode, otherwise not show the root menu
 * redirect: noRedirect           if set noRedirect will no redirect in the breadcrumb
 * name:'router-name'             the name is used by <keep-alive> (must set!!!)
 * meta : {
    roles: ['admin','editor']    control the page roles (you can set multiple roles)
    title: 'title'               the name show in sidebar and breadcrumb (recommend set)
    icon: 'svg-name'/'el-icon-x' the icon show in the sidebar
    breadcrumb: false            if set false, the item will hidden in breadcrumb(default is true)
    activeMenu: '/example/list'  if set path, the sidebar will highlight the path you set
  }
 */

/**
 * constantRoutes
 * a base page that does not have permission requirements
 * all roles can be accessed
 * 此处路由每个角色都可以访问
 */
export const constantRoutes = [
  {
    path: '/login',
    component: () => import('@/views/login/index'),
    hidden: true
  },
  {
    path: '/404',
    component: () => import('@/views/404'),
    hidden: true
  },
  {
    path: '/',
    component: Layout,
    redirect: '/dashboard',
    children: [{
      path: 'dashboard',
      name: 'DashBoard', //与组件中的名称命名保持一致
      component: () => import('@/views/dashboard/index'),
      meta: {
        title: '主页',
        icon: 'dashboard',
        affix: true
      }
    }],
  }
]
/**
 * 根据role动态构建路由
 */
export const asyncRoutes = [
  {
    path: '/manage',
    component: Layout,
    alwaysShow: true,
    redirect: '/manage/users',
    name:'系统管理',
    meta: {
      title: '系统管理',//一级模块名称
      icon: 'el-icon-s-tools',
      menu: 'system-manage'
    },
    children: [{
        path: 'users',
        name:'UserList',
        component: () => import('@/views/user/userList'),
        meta: {
          title: '用户管理',
          icon: 'el-icon-user-solid',
          menu: 'user-manage'
        }
      },
      {
        path: '/user/modify_self',
        name:'EditUser',
        component: () => import('@/views/user/editSelf'),
        meta: {
          title: '修改用户信息'
        },
        hidden: true
      },
      {
        path: '/user/add',
        name:'AddUser',
        component: () => import('@/views/user/userAdd'),
        meta: {
          title: '新增用户',
          menu: 'user-add'
        },
        hidden: true
      },
      {
        path: 'roles',
        name: 'RoleList',
        component: () => import('@/views/role/roleList'),
        meta: {
          title: '角色管理',
          icon: 'peoples',
          menu: 'role-manage'
        }
      },
      {
        path: '/role/edit/:id',
        name:'EditRole',
        component: () => import('@/views/role/roleEdit'),
        hidden: true,
        meta: {
          title: '角色编辑',
          menu: 'role-edit'
        }
      },
      {
        path: 'perms',
        name:'PermList',
        component: () => import('@/views/perm/permList'),
        meta: {
          title: '权限管理',
          icon: 'eye-open',
          menu: 'perm-manage'
        }
      },
      {
        path: 'menus',
        name:'MenumList', //与组件名称对应
        component: () => import('@/views/menu/menuList'),
        meta: {
          title: '菜单管理',
          icon: 'list',
          menu: 'menu-manage'
        }
      },
      {
        path: 'records',
        component: () => import('@/views/record/recordList'),
        meta: {
          title: '操作记录',
          icon: 'el-icon-postcard',
          menu: 'record-manage'
        }
      }
    ]
  },
  {
    path: '/utils',
    component: Layout,
    name: '实用小工具',
    alwaysShow: true,
    meta: {
      title: '实用小工具',
      icon: 'el-icon-magic-stick',
      menu: 'small-utils'
    },
    redirect: '/utils/server',
    children: [
      {
        path: 'server',
        name: 'ServerList',
      component: () => import('@/views/server/serverList'),
      meta: {
        title: '服务器管理',
        icon: 'el-icon-cloudy',
        menu: 'server-manage'
      }
    },
    {
      path: '/server/add',
      name: 'AddServer',
      component: () => import('@/views/server/serverAdd'),
      meta: {
        title: '新增服务器',
        menu: 'server-add'
      },
      //hidden：true 默认不在侧边栏显示 默认为false
      hidden: true
    },
    {
      path: 'http_test',
      name: 'HttpTest',
      component: () => import('@/views/httptest/httptest'),
      meta: {
        title: 'http接口测试',
        icon: 'el-icon-cpu',
        menu: 'http-test'
      }
      
    }
  ]
},
{
  path: '/auto',
  component: Layout,
  name: '自动化管理',
  alwaysShow: true,
  meta: {
    title: '自动化管理',
    icon: 'el-icon-help',
    menu: 'auto-manage'
  },
  redirect: '/auto/project',
  children: [{
    path: 'project',
    name: 'ProjectList',
      component: () => import('@/views/auto/projectList'),
      meta: {
        title: '项目管理',
        icon: 'el-icon-suitcase',
        menu: 'project-manage'
      }
    },
    {
      path: 'module',
      name: 'ModuleList',
      component: () => import('@/views/auto/moduleList'),
      meta: {
        title: '模块管理',
        icon: 'el-icon-s-grid',
        menu: 'module-manage'
      }

    },
    {
      path: 'testcase',
      name: 'TestCaseList',
      component: () => import('@/views/auto/case/testcaseList'),
      meta: {
        title: '用例管理',
        icon: 'el-icon-notebook-1',
        menu: 'testcase-manage'
      }

    },

    {
      name: 'EnvironmentList',
      path: 'env',
      component: () => import('@/views/auto/environmentList'),
      meta: {
        title: '环境配置',
        icon: 'el-icon-tickets',
        menu: 'env-config'
      }

    },
  ]

},

// {
//   path: '/cmdb',
//   name: '资源管理',
//   component: Layout,
//   alwaysShow: true,
//   meta: {
//     title: '资源管理',
//     icon: 'cc-architecture',
//     menu: 'cmdb-manage'
//   },
//   redirect: '/cmdb/model',
//   children: [{
//       path: 'model',
//       component: () => import('@/views/cmdb/model'),
//       meta: {
//         title: '模型',
//         icon: 'cc-module',
//         menu: 'cmdb-model'
//       }
//     },
//     {
//       path: 'edit_type/:id',
//       hidden: true,
//       component: () => import('@/views/cmdb/editModel'),
//       meta: {
//         title: '修改模型',
//         menu: 'cmdb-type-edit'
//       }
//     },
//     {
//       path: 'instance',
//       component: () => import('@/views/cmdb/instance'),
//       meta: {
//         title: '实例',
//         icon: 'cc-vmware',
//         menu: 'cmdb-instance'
//       }
//     },
//     {
//       path: 'all_instances/:id',
//       hidden: true,
//       component: () => import('@/views/cmdb/allInstance'),
//       meta: {
//         title: '所有实例',
//         menu: 'cmdb-all-instance'
//       }
//     }
//   ]
// },

  {
    name: 'web_ssh',
    path: '/server/web_ssh/:server_id',
    component: () => import('@/views//server/webSSH'),
    hidden: true,
    meta: {
      title: 'terminal',
      menu: 'server-web-ssh'
    }
  },
  // 404 page must be placed at the end !!!
  {
    path: '*',
    redirect: '/404',
    hidden: true
  }
]

const createRouter = () => new Router({
  // mode: 'history', // require service support
  scrollBehavior: () => ({
    y: 0
  }),
  routes: constantRoutes
})

const router = createRouter()

// Detail see: https://github.com/vuejs/vue-router/issues/1234#issuecomment-357941465
export function resetRouter() {
  const newRouter = createRouter()
  router.matcher = newRouter.matcher // reset router
}

export default router
