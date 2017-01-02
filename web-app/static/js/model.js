/**
 * Created by adrie on 02/01/2017.
 */

class User{
  constructor() {
    this.userName = "";
    this.password = "";
    this.email = "";
    this.bio = "";
    this.birthDate = "";
  }

  fillUser(username, email, bio, birthDate, password){
    this.userName = username;
    this.password = password;
    this.email = email;
    this.bio = bio;
    this.birthDate = birthDate;
  }

  checkBeforeSignIn(confirmPassword){
    return !(confirmPassword == undefined || confirmPassword != this.password || this.userName == undefined || this.userName == "" || this.password == undefined || this.password == "");

  }

  checkBeforeLogin(){
    return !(this.userName == undefined || this.userName == "" || this.password == undefined || this.password == "");

  }
}

export { User };
