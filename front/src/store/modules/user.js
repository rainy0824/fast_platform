import { login, logout, getInfo, edit } from '@/api/user'
import { getToken, setToken, removeToken } from '@/utils/auth'
import { resetRouter } from '@/router'

const getDefaultState = () => {
  return {
    token: getToken(),
    name: '',
    avatar: '',
    menus: []
  }
}

const state = getDefaultState()

const mutations = {
  RESET_STATE: (state) => {
    Object.assign(state, getDefaultState())
  },
  SET_TOKEN: (state, token) => {
    state.token = token
  },
  SET_NAME: (state, name) => {
    state.name = name
  },
  SET_AVATAR: (state, avatar) => {
    state.avatar = avatar
  },
  SET_MENUS: (state, menus) => {
    state.menus = menus
  }
}

const actions = {
  // user login
  login({ commit }, userInfo) {
    console.log('user login actions 被调用了',commit,userInfo)
    const { username, password } = userInfo
    return new Promise((resolve, reject) => {
      login({ username: username.trim(), password: password }).then(response => {
        const data = response
        console.log('adw:',this)
        commit('SET_TOKEN', data.access_token)
        setToken(data.access_token)
        resolve(response)
      }).catch(error => {
        reject(error)
      })
    })
  },

  // get user info
  getInfo({ commit, state }) {
    return new Promise((resolve, reject) => {
      getInfo().then(response => {
        const data = response
        if (!data) {
          return reject('Verification failed, please Login again.')
        }

        const { nick_name, avatar, menus } = data
        if (!menus || menus.length <= 0) {
          return reject('用户未分配菜单') //将响应结果返回给.catch
        }
        commit('SET_NAME', nick_name)
        commit('SET_AVATAR', avatar)
        commit('SET_MENUS', menus)
        resolve(data)
      }).catch(error => {
        reject(error)
      })
    })
  },
  editSelf({ commit, state }, editInfo) {
    const { nickname } = editInfo
    return new Promise((resolve, reject) => {
      edit(editInfo).then(response => {
        commit('SET_NAME', nickname)
        resolve(response) //将响应结果返回给.then
      }).catch(error => {
        reject(error)
      })
    })
  },

  // user logout
  logout({ commit, state ,dispatch }) {
    return new Promise((resolve, reject) => {
      logout(state.token)
      .then(() => {
        removeToken() // must remove  token  first
        resetRouter()
        commit('RESET_STATE')
        dispatch('tagsView/delAllViews', null, { root: true })
        resolve()
      }).catch(error => {
        reject(error)
      })
    })
  },

  // remove token
  resetToken({ commit }) {
    return new Promise(resolve => {
      removeToken() // must remove  token  first
      commit('RESET_STATE')
      resolve()
    })
  },
  // edit user info
  editUser({ commit }, userInfo) {
    return new Promise((resolve, reject) => {
      edit(userInfo).then(response => {
        resolve(response.data)
      }).catch(error => {
        reject(error)
      })
    })
  }
}

export default {
  namespaced: true,
  state,
  mutations,
  actions
}

