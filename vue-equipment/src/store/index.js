import { createApp } from 'vue'
import { createStore } from 'vuex'

// Create a new store instance.
const store = createStore({
    state () {
        return {
            searchFor: '',
            equipmentTypes: [],
            equipmentList: [],
            backendUrl: 'http://127.0.0.1:8000/api',
            username: '',
            accessToken: null,
            refreshToken: null,
        }
    },
    mutations: {
        updateStorage (state, { access, refresh, username }) {
            state.accessToken = access
            state.refreshToken = refresh
            state.username = username
        },
        destroyToken (state) {
            state.accessToken = null
            state.refreshToken = null
        },
        setEquipmentTypes(state, {types}){
            state.equipmentTypes = types['results']
        }
    },
    actions: {
        userLogout (context) {
            if (context.getters.loggedIn) {
                context.commit('destroyToken')
            }
        },
        async userLogin (context, userCredentials) {
            const backendUrl = context.getters.getServerUrl + '/user/login/'
            try{
                const response = await fetch(
                    backendUrl, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify(userCredentials)
                    }
                )
                let status = response.status
                if (status === 200) {
                    console.log("Авторизован")
                    let result = await response.json()
                    context.commit('updateStorage', { access: result['tokens']['access'],
                        refresh: result['tokens']['refresh'], username: result['username']})
                } else if (status === 401) {
                    console.log("Неверные логин и пароль")
                } else {
                    console.log("Ошибка в данных при авторизации")
                }
            }  catch (err) {
                console.log('Ошибка при авторизации: ', err);
            }
        },
        async loadEquipmentTypes(context) {
            const backendUrl = context.getters.getServerUrl + '/equipment-type'
            try {
                const response = await fetch(backendUrl,{
                    method: 'GET',
                    headers: {
                        'Content-Type': 'application/json',
                        'Authorization': `Bearer ${context.state.accessToken}`
                    }
                })
                if (response.status === 200) {
                    let result = await response.json()
                    context.commit('setEquipmentTypes', {types: result})
                }
            } catch (err) {
                console.log(err);
            }
        },
    },
    modules: {},
    getters: {
        getServerUrl(state) {
            return state.backendUrl
        },
        loggedIn(state) {
            return state.accessToken != null
        }
    }
})

export default store