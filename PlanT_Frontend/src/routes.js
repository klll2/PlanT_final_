/*!

=========================================================
* Paper Dashboard React - v1.3.2
=========================================================

* Product Page: https://www.creative-tim.com/product/paper-dashboard-react
* Copyright 2023 Creative Tim (https://www.creative-tim.com)

* Licensed under MIT (https://github.com/creativetimofficial/paper-dashboard-react/blob/main/LICENSE.md)

* Coded by Creative Tim

=========================================================

* The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

*/
// import Dashboard from "views/Dashboard.js";
import Notifications from "views/Notifications.js";
import Icons from "views/Icons.js";
// import Typography from "views/Typography.js";
import TableList from "views/Tables.js";
import Login from "views/LoginGoogle";
import Mypage from "views/Mypage";
// import UserPage from "views/User.js";
// import UpgradeToPro from "views/Upgrade.js";

var routes = [
  // {
  //   path: "/dashboard",
  //   name: "Dashboard",
  //   icon: "nc-icon nc-bank",
  //   component: <Dashboard />,
  //   layout: "/admin",
  // },
  {
    path: "/mypage",
    name: "My Page",
    icon: "nc-icon nc-diamond",
    component: <Mypage />,
    layout: "/admin",
  },
  {
    path: "/icons",
    name: "Input Page",
    icon: "nc-icon nc-diamond",
    component: <Icons />,
    layout: "/admin",
  },
  // {
  //   path: "/tables",
  //   name: "Input Page(2)",
  //   icon: "nc-icon nc-tile-56",
  //   component: <TableList />,
  //   layout: "/admin",
  // },
  {
    path: "/plans",
    name: "Output Page",
    icon: "nc-icon nc-bell-55",
    component: <Notifications />,
    layout: "/admin",
  },
  {  
    path: "/login",
    name: "Login",
    icon: "nc-icon nc-bell-55",
    component: <Login />,
    layout: "/login",
    hidden: true,
  },
  // {
  //   path: "/pla1",
  //   name: "User Profile",
  //   icon: "nc-icon nc-single-02",
  //   component: <UserPage />,
  //   layout: "/admin",
  // },
  // {
  //   path: "/typography",
  //   name: "Typography",
  //   icon: "nc-icon nc-caps-small",
  //   component: <Typography />,
  //   layout: "/admin",
  // },
  // {
  //   pro: true,
  //   path: "/upgrade",
  //   name: "Upgrade to PRO",
  //   icon: "nc-icon nc-spaceship",
  //   component: <UpgradeToPro />,
  //   layout: "/admin",
  // },
];
export default routes;
