import router from '../router'


export default{
    state:{
        name:window.localStorage.getItem('name')?window.localStorage.getItem('name'):null,
        email:window.localStorage.getItem('email')?window.localStorage.getItem('email'):null,
        token:window.localStorage.getItem('token')?window.localStorage.getItem('token'):null,
    },
    getters:{
        name:(state)=>{
            if(state.name==null){
                let sessionUser = localStorage.getItem("name");
                if(sessionUser !=null)
                {
                    state.name = JSON.parse(sessionUser)
                    return sessionUser
                }
            }
            return state.name
        },
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
        setEmail(state, email){
            localStorage.setItem("email",email)
            state.token=email
        },
        setUser(state, name){
            state.name=name
            localStorage.setItem("name",name)
        },
        logout(state){
            state.name=null
            state.token=null
            state.email=null
            localStorage.removeItem("token")
            localStorage.removeItem("name")
            localStorage.removeItem("email")
            router.push('/login')
        }
    },
    actions:{},
}