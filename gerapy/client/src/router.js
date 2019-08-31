import Vue from 'vue'
import Router from 'vue-router'

Vue.use(Router)

const router = new Router({
	mode: 'history',
	routes: [
		{
			path: '/',
			name: 'home',
			component: () => import('./views/home/Index.vue')
		},
		// client management
		{
			path: '/client',
			name: 'clientIndex',
			component: () => import('./views/client/Index.vue')
		},
		{
			path: '/client/create',
			name: 'clientCreate',
			component: () => import('./views/client/Create.vue')
		},
		{
			path: '/client/:id/edit',
			name: 'clientEdit',
			component: () => import('./views/client/Edit.vue')
		},
		{
			path: '/client/:id/schedule',
			name: 'clientSchedule',
			component: () => import('./views/client/Schedule.vue')
		},
		// project management
		{
			path: '/project',
			name: 'projectIndex',
			component: () => import('./views/project/Index.vue')
		},
		{
			path: '/project/:name/edit',
			name: 'projectEdit',
			component: () => import('./views/project/Edit.vue')
		},
		{
			path: '/project/:name/deploy',
			name: 'projectDeploy',
			component: () => import('./views/project/Deploy.vue')
		},
		{
			path: '/project/:name/configure',
			name: 'projectConfigure',
			component: () => import('./views/project/Configure.vue')
		},
		{
			path: '/project/:name/configure2',
			name: 'projectConfigure2',
			component: () => import('./views/project/Configure2.vue')
		},
		// task management
		{
			path: '/task',
			name: 'taskIndex',
			component: () => import('./views/task/Index.vue')
		},
		{
			path: '/task/:id/create',
			name: 'taskCreate',
			component: () => import('./views/task/Create.vue')
		},
		{
			path: '/task/:id/edit',
			name: 'taskEdit',
			component: () => import('./views/task/Edit.vue')
		},
		{
			path: '/task/:id/status',
			name: 'taskStatus',
			component: () => import('./views/task/Status.vue')
		}

	]
})

export default router