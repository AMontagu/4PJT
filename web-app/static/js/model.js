/**
 * Created by adrie on 02/01/2017.
 */

class Notification {
  constructor() {
    this.dateRead = null;
    this.groupName = "";
    this.senderName = "";
    this.text = "";
  }

  copyConstructor(object) {
    if (typeof object == "string") {
      object = JSON.parse(object);
    }

    /*if(object.hasOwnProperty('message')){
     if(object.message == "string"){
     object.message = JSON.parse(object.message);
     }
     }*/

    //console.log(object);
    this.dateRead = object.dateRead;
    this.groupName = object.message.qwirkGroup;
    this.senderName = object.message.qwirkUser;
    this.text = object.message.text;
  }
}

class Contact {
  constructor() {
    this.qwirkGroup = new QwirkGroup();
    this.qwirkUser = new QwirkUser();
    this.status = "";
  }

  copyConstructor(object) {
    if (typeof object === "string") {
      object = JSON.parse(object);
    }

    this.qwirkGroup = object.qwirkGroup;
    this.qwirkUser.copyConstructor(object.qwirkUser);
    this.status = object.status;
  }
}

class QwirkGroup {
  constructor() {
    this.name = "";
    this.private = true;
    this.isContactGroup = true;
    this.admin = []
  }
}

class User {
  constructor() {
    this.username = "";
    this.email = "";
    this.password = "";
    this.first_name = "";
    this.last_name = "";
  }

  copyConstructor(object) {
    if (typeof object === "string") {
      object = JSON.parse(object);
    }
    //console.log(object);
    this.username = object.username;
    this.email = object.email;
    this.first_name = object.first_name;
    this.last_name = object.last_name;
  }

  checkBeforeSignIn(confirmPassword) {
    return !(confirmPassword == undefined || confirmPassword != this.password || this.username == undefined || this.username == "" || this.password == undefined || this.password == "");

  }

  checkBeforeLogin() {
    return !(this.username == undefined || this.username == "" || this.password == undefined || this.password == "");

  }
}

class QwirkUser {
  constructor() {
    this.user = new User();
    this.contacts = [];
    this.qwirkGroups = [];
    this.bio = "";
    this.birthDate = "";
    this.notifications = [];
    this.avatar = "";
  }

  copyConstructor(object) {
    if (typeof object == "string") {
      object = JSON.parse(object);
    }
    console.log(object);
    this.user.copyConstructor(object.user);
    //this.user = object.user;
    //console.log(this.user);
    this.bio = object.bio;
    this.birthDate = object.birthDate;
    this.qwirkGroups = object.qwirkGroups;
    this.contacts = object.contacts;
    this.avatar = object.avatar;

    if (typeof object.notifications !== 'undefined' && object.notifications.length > 0) {
      object.notifications.forEach((notification) => {
        let notif = new Notification();
        notif.copyConstructor(notification);
        this.notifications.push(notif);
      })
    }
  }

  fillUser(user, bio, birthDate, groups, contacts) {
    this.user = user;
    this.bio = bio;
    this.birthDate = birthDate;
    this.qwirkGroups = qwirkGroups;
    this.contacts = contacts;
  }

  fillUserSignin(user, bio, birthDate) {
    this.user = user;
    this.bio = bio;
    this.birthDate = birthDate;
  }

  checkBeforeSignIn(confirmPassword) {
    return this.user.checkBeforeSignIn(confirmPassword)

  }

  checkBeforeLogin() {
    return this.user.checkBeforeLogin()

  }

  existContact(newContact) {
    for (let i = 0; i < this.contacts.length; i++) {
      if (newContact.qwirkGroup.name === this.contacts[i].qwirkGroup.name) {
        if(this.contacts[i].status !== "Refuse"){
          return true;
        }
      }
    }
    return false;
  }

  existGroup(newGroup) {
    for (let i = 0; i < this.qwirkGroups.length; i++) {
      if (newGroup.name === this.qwirkGroups[i].name) {

        return true;
      }
    }

    return false;
  }
}

class Message {
  constructor() {
    this.qwirkUser = new QwirkUser();
    this.qwirkGroup = new QwirkGroup();
    this.text = "";
    this.dateTime = new Date();
    this.type = "";
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

class GroupInformations {
  constructor() {
    this.isPrivate = true;
    this.isContactGroup = true;
    this.isAdmin = false;
    this.qwirkUsers = [];
    this.titleGroupName = "";
    this.statusContact = "";
  }

  copyConstructor(object) {
    if (typeof object == "string") {
      object = JSON.parse(object);
    }
    console.log(object);
    this.isPrivate = object.isPrivate;
    this.isContactGroup = object.isContactGroup;
    this.isAdmin = object.isAdmin;
    /*if(typeof object.qwirkUsers == "string"){
     object.qwirkUsers = JSON.parse(object.qwirkUsers);
     }*/
    this.qwirkUsers = object.qwirkUsers;
    this.titleGroupName = object.titleGroupName;
    this.statusContact = object.statusContact;
  }

}

export {User, QwirkUser, QwirkGroup, Message, GroupInformations, Notification, Contact};
