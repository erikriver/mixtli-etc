import DashboardPage from "views/Dashboard/Dashboard.jsx";
import UserProfile from "views/UserProfile/UserProfile.jsx";
import TableList from "views/TableList/TableList.jsx";
import Typography from "views/Typography/Typography.jsx";
import Icons from "views/Icons/Icons.jsx";
import Maps from "views/Maps/Maps.jsx";
import NotificationsPage from "views/Notifications/Notifications.jsx";

import {
  Dashboard,
  Person,
  ContentPaste,
  LibraryBooks,
  BubbleChart,
  LocationOn,
  Notifications
} from "material-ui-icons";

const appRoutes = [
  {
    path: "/intro",
    sidebarName: "Inicio",
    navbarName: "Inicio",
    icon: LibraryBooks,
    component: Typography
  },
  {
    path: "/dashboard1",
    sidebarName: "Dashboard",
    navbarName: "Material Dashboard",
    icon: Dashboard,
    component: DashboardPage
  },
  {
    path: "/table",
    sidebarName: "Indicador",
    navbarName: "Indicador",
    icon: ContentPaste,
    component: TableList
  },
  { redirect: true, path: "/", to: "/intro", navbarName: "Redirect" }
];

export default appRoutes;
