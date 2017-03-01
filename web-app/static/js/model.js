/**
 * Created by adrie on 02/01/2017.
 */

class QwirkGroup{
  constructor() {
    this.name = "";
    this.private = true;
  }
}

class User{
  constructor() {
    this.username = "";
    this.email = "";
    this.password = "";
    this.firstname = "";
    this.lastname = "";
  }

  checkBeforeSignIn(confirmPassword){
    return !(confirmPassword == undefined || confirmPassword != this.password || this.username == undefined || this.username == "" || this.password == undefined || this.password == "");

  }

  checkBeforeLogin(){
    return !(this.userName == undefined || this.userName == "" || this.password == undefined || this.password == "");

  }
}

class QwirkUser{
  constructor() {
    this.user = new User();
    this.contacts = [];
    this.qwirkGroups = [];
    this.bio = "";
    this.birthDate = "";
  }

  copyConstructor(object){
    if(typeof object == "string"){
      object = JSON.parse(object);
    }
    console.log(object);
    this.user = object.user;
    this.bio = object.bio;
    this.birthDate = object.birthDate;
    this.qwirkGroups = object.qwirkGroups;
    this.contacts = object.contacts;
  }

  fillUser(user, bio, birthDate, groups, contacts){
    this.user = user;
    this.bio = bio;
    this.birthDate = birthDate;
    this.qwirkGroups = qwirkGroups;
    this.contacts = contacts;
  }

  fillUserSignin(user, bio, birthDate){
    this.user = user;
    this.bio = bio;
    this.birthDate = birthDate;
  }

  checkBeforeSignIn(confirmPassword){
    return this.user.checkBeforeSignIn(confirmPassword)

  }

  checkBeforeLogin(){
    return this.user.checkBeforeLogin()

  }
}

class Message{
  constructor() {
    this.qwirkUser = new QwirkUser();
    this.qwirkGroup = new QwirkGroup();
    this.text = "";
    this.dateTime = new Date();
  }

  /*copyConstructor(object){
    if(typeof object == "string"){
      object = JSON.parse(object);
    }
    console.log(object);
    this.user = object.user;
    this.bio = object.bio;
    this.birthDate = object.birthDate;
    this.qwirkGroups = object.qwirkGroups;
    this.contacts = object.contacts;
  }*/

}

export { User, QwirkUser, QwirkGroup, Message };
