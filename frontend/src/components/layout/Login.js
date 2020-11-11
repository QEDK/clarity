import React,{useState} from 'react';
import firebase from 'firebase'

const Login = () => {
    var [token, setToken] = useState('')
    var [user, setUser] = useState('')
    var [email, setEmail] = useState('')

    var provider = new firebase.auth.GoogleAuthProvider();
    function handleLogin (event) {
        firebase.auth().signInWithPopup(provider).then(function(result) {
             setToken(result.credential.accessToken);
             setUser(result.user);
             if(!token){
                 this.history.push('/login')
             } else {
                 this.history.push('/')
             }
          }).catch(function(error) {
             setEmail(error.email);
          });

          console.log('user log = ', user)
          console.log('token log = ', token)
          console.log('email log = ', email)
    }
    return (
        <section className='content'>
            <h1 style={{ 'marginTop': '100px', 'textAlign': 'center' }}>Login</h1>
            <br />
            <button type='submit' onClick={handleLogin} style={{'width':'200px', 'padding':'10px', 'alignSelf': 'center', 'marginTop':'30px', 'margin':'auto'}}>Login</button>
        </section>
    )
}

export default Login;