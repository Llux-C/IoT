import router from '../router'


export default{
    state:{
        email:window.localStorage.getItem('email')?window.localStorage.getItem('email'):null,
        token:window.localStorage.getItem('token')?window.localStorage.getItem('token'):null,
    },
    getters:{
        email:(state)=>{
            if(state.email==null){
                let sessionUser = localStorage.getItem("email");
                if(sessionUser !=null)
                {
                    state.email = JSON.parse(sessionUser)
                    return sessionUser
                }
            }
            return state.email
        },
        token:(state)=>{
            if(state.token == null)
            {
                let sessionToken = localStorage.getItem("token")
                if(sessionToken != null)
                {
                    state.token=JSON.parse(sessionToken)
                    return sessionToken
                }
            }
            return state.token
        }
    },
    mutations:{
        setToken(state, token){
            localStorage.setItem("token",token)
            state.token=token
        },
        setUser(state, email){
            state.email=email
            localStorage.setItem("email",email)
        },
        logout(state){
            state.email=null
            state.token=null
            localStorage.removeItem("token")
            localStorage.removeItem("email")
            router.push('/login')
        }
    },
    actions:{},
}