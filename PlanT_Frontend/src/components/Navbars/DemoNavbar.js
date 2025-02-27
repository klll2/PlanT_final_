// /*!

// =========================================================
// * Paper Dashboard React - v1.3.2
// =========================================================

// * Product Page: https://www.creative-tim.com/product/paper-dashboard-react
// * Copyright 2023 Creative Tim (https://www.creative-tim.com)

// * Licensed under MIT (https://github.com/creativetimofficial/paper-dashboard-react/blob/main/LICENSE.md)

// * Coded by Creative Tim

// =========================================================

// * The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

// */
// import React from "react";
// import { useLocation } from "react-router-dom";
// import {
//   Collapse,
//   Navbar,
//   NavbarToggler,
//   NavbarBrand,
//   Nav,
//   // NavItem,
//   Dropdown,
//   DropdownToggle,
//   DropdownMenu,
//   DropdownItem,
//   Container,
//   // InputGroup,
//   // InputGroupText,
//   // InputGroupAddon,
//   // Input,
// } from "reactstrap";

// import routes from "routes.js";
// import axios from "axios";
// import { useCookies } from 'react-cookie';


// function Header(props) {
//   const [isOpen, setIsOpen] = React.useState(false);
//   const [dropdownOpen, setDropdownOpen] = React.useState(false);
//   const [color, setColor] = React.useState("transparent");
//   const [userinfo, setUserinfo] = React.useState(null);
//   const [cookies, setCookie, removeCookie] = useCookies(['trvlr_id', 'trvlr_email']);
//   const sidebarToggle = React.useRef();
//   const location = useLocation();

//   // const getUserState = async () => {
//   //   try {
//   //     const response = await axios.get('http://localhost:8000/account/state/');
//   //     // 응답 데이터에서 사용자 정보를 상태로 설정
//   //     setUserinfo(response.data);
//   //   } catch (error) {
//   //     // 요청 실패 시 에러를 콘솔에 출력
//   //     console.error("Failed to fetch user:", error);
//   //   }
//   // };

//   // React.useEffect(() => {
//   //   getUserState();
//   //   console.log(userinfo)
//   // }, [location]);

//   const handleLogout = () => {
//     // try {
//     //   const response = await axios.post("http://localhost:8000/account/logout/", {  });

//     //   if (response.data.success) {
//         // 로그아웃 성공 시 로그인 페이지로 이동
//     removeCookie('trvlr_id');
//     removeCookie('trvlr_email');
//     window.location.href = 'http://localhost:3000/login/login';
//   //     } else if (response.data.error) {
//   //       // 로그아웃 실패 시 에러 메시지 출력
//   //       alert(response.data.error);
//   //     }
//   //   } catch (error) {
//   //     console.error("Failed to logout:", error);
//   //     // 로그아웃 실패 시 에러 메시지 출력
//   //     alert("Logout failed. Please try again.");
//   //   }
//   };

//   const toggle = () => {
//     if (isOpen) {
//       setColor("transparent");
//     } else {
//       setColor("dark");
//     }
//     setIsOpen(!isOpen);
//   };
//   const dropdownToggle = (e) => {
//     setDropdownOpen(!dropdownOpen);
//   };
//   const getBrand = () => {
//     let brandName = "Default Brand";
//     routes.map((prop, key) => {
//       if (window.location.href.indexOf(prop.layout + prop.path) !== -1) {
//         brandName = prop.name;
//       }
//       return null;
//     });
//     return brandName;
//   };
//   const openSidebar = () => {
//     document.documentElement.classList.toggle("nav-open");
//     sidebarToggle.current.classList.toggle("toggled");
//   };
//   // function that adds color dark/transparent to the navbar on resize (this is for the collapse)
//   const updateColor = () => {
//     if (window.innerWidth < 993 && isOpen) {
//       setColor("dark");
//     } else {
//       setColor("transparent");
//     }
//   };
//   React.useEffect(() => {
//     window.addEventListener("resize", updateColor.bind(this));
//   });
//   React.useEffect(() => {
//     if (
//       window.innerWidth < 993 &&
//       document.documentElement.className.indexOf("nav-open") !== -1
//     ) {
//       document.documentElement.classList.toggle("nav-open");
//       sidebarToggle.current.classList.toggle("toggled");
//     }
//   }, [location]);
//   return (
//     // add or remove classes depending if we are on full-screen-maps page or not
//     <Navbar
//       color={
//         location.pathname.indexOf("full-screen-maps") !== -1 ? "dark" : color
//       }
//       expand="lg"
//       className={
//         location.pathname.indexOf("full-screen-maps") !== -1
//           ? "navbar-absolute fixed-top"
//           : "navbar-absolute fixed-top " +
//             (color === "transparent" ? "navbar-transparent " : "")
//       }>
//       <Container fluid>
//         <div className="navbar-wrapper">
//           <div className="navbar-toggle">
//             <button
//               type="button"
//               ref={sidebarToggle}
//               className="navbar-toggler"
//               onClick={() => openSidebar()}
//             >
//               <span className="navbar-toggler-bar bar1" />
//               <span className="navbar-toggler-bar bar2" />
//               <span className="navbar-toggler-bar bar3" />
//             </button>
//           </div>
//           <NavbarBrand href="/">{getBrand()}</NavbarBrand>
//         </div>
//         <NavbarToggler onClick={toggle}>
//           <span className="navbar-toggler-bar navbar-kebab" />
//           <span className="navbar-toggler-bar navbar-kebab" />
//           <span className="navbar-toggler-bar navbar-kebab" />
//         </NavbarToggler>
//         <Collapse isOpen={isOpen} navbar className="justify-content-end">
//           {/* <form>
//             <InputGroup className="no-border">
//               <Input placeholder="Search..." />
//               <InputGroupAddon addonType="append">
//                 <InputGroupText>
//                   <i className="nc-icon nc-zoom-split" />
//                 </InputGroupText>
//               </InputGroupAddon>
//             </InputGroup>
//           </form> */}
//           <Nav navbar> 
//           <Dropdown
//             nav
//             isOpen={dropdownOpen}
//             toggle={(e) => dropdownToggle(e)}
//           >
//             <DropdownToggle caret nav>
//               <i className="nc-icon nc-circle-10" />
//               <p>
//                 {cookies ? (
//                   <span className="nav-link">{cookies.trvlr_email}</span>
//                 ) : (
//                   <span>Account</span>
//                 )}
//               </p>
//             </DropdownToggle>
//             <DropdownMenu right>
//               {cookies ? (
//                 <DropdownItem tag="a" onClick={handleLogout}>
//                   Logout
//                 </DropdownItem>
//               ) : (
//                 <DropdownItem href="http://localhost:3000/login/login">
//                   Login
//                 </DropdownItem>
//               )}
//             </DropdownMenu>
//           </Dropdown>

//           {/*  <Dropdown
//               nav
//               isOpen={dropdownOpen}
//               toggle={(e) => dropdownToggle(e)}
//             >
//               <DropdownToggle caret nav>
//                 <i className="nc-icon nc-circle-10" />
//                 <p>
//                   {user ? (
//                 <span className="nav-link">{user.email}</span>
//               ) : (
//                 <span className="d-lg-none d-md-block">Account</span>
//               )}
//                 </p>
//               </DropdownToggle>
//               <DropdownMenu right>
//                 <DropdownItem tag="a">Action</DropdownItem>
//                 <DropdownItem tag="a">Another Action</DropdownItem>
//                 <DropdownItem tag="a">Something else here</DropdownItem>
//               </DropdownMenu>
//             </Dropdown>
//             <NavItem>
//               <Link to="#pablo" className="nav-link btn-rotate">
//                 <i className="nc-icon nc-settings-gear-65" />
//                 <p>
//                   <span className="d-lg-none d-md-block">Account</span>
//                 </p>
//               </Link>
//               </NavItem> */}
//           </Nav> 
//         </Collapse>
//       </Container>
//     </Navbar>
//   );
// }

// export default Header;


import React from "react";
import { useLocation } from "react-router-dom";
import {
  Collapse,
  Navbar,
  NavbarToggler,
  NavbarBrand,
  Nav,
  // NavItem,
  Dropdown,
  DropdownToggle,
  DropdownMenu,
  DropdownItem,
  Container,
  // InputGroup,
  // InputGroupText,
  // InputGroupAddon,
  // Input,
} from "reactstrap";

import routes from "routes.js";
import axios from "axios";

function Header(props) {
  const [isOpen, setIsOpen] = React.useState(false);
  const [dropdownOpen, setDropdownOpen] = React.useState(false);
  const [color, setColor] = React.useState("transparent");
  const [userinfo, setUserinfo] = React.useState(null);
  const sidebarToggle = React.useRef();
  const location = useLocation();

  // const getUserState = async () => {
  //   try {
  //     const response = await axios.get('http://localhost:8000/account/state/');
  //     // 응답 데이터에서 사용자 정보를 상태로 설정
  //     setUserinfo(response.data);
  //   } catch (error) {
  //     // 요청 실패 시 에러를 콘솔에 출력
  //     console.error("Failed to fetch user:", error);
  //   }
  // };

  // React.useEffect(() => {
  //   getUserState();
  //   console.log(userinfo)
  // }, [location]);

  const handleLogout = () => {

    localStorage.clear();

    window.location.href = 'http://localhost:3000/login/login';
    
  };

  const toggle = () => {
    if (isOpen) {
      setColor("transparent");
    } else {
      setColor("dark");
    }
    setIsOpen(!isOpen);
  };
  const dropdownToggle = (e) => {
    setDropdownOpen(!dropdownOpen);
  };
  const getBrand = () => {
    let brandName = "Default Brand";
    routes.map((prop, key) => {
      if (window.location.href.indexOf(prop.layout + prop.path) !== -1) {
        brandName = prop.name;
      }
      return null;
    });
    return brandName;
  };
  const openSidebar = () => {
    document.documentElement.classList.toggle("nav-open");
    sidebarToggle.current.classList.toggle("toggled");
  };
  // function that adds color dark/transparent to the navbar on resize (this is for the collapse)
  const updateColor = () => {
    if (window.innerWidth < 993 && isOpen) {
      setColor("dark");
    } else {
      setColor("transparent");
    }
  };
  React.useEffect(() => {
    window.addEventListener("resize", updateColor.bind(this));
  });
  React.useEffect(() => {
    if (
      window.innerWidth < 993 &&
      document.documentElement.className.indexOf("nav-open") !== -1
    ) {
      document.documentElement.classList.toggle("nav-open");
      sidebarToggle.current.classList.toggle("toggled");
    }
  }, [location]);
  return (
    // add or remove classes depending if we are on full-screen-maps page or not
    <Navbar
      color={
        location.pathname.indexOf("full-screen-maps") !== -1 ? "dark" : color
      }
      expand="lg"
      className={
        location.pathname.indexOf("full-screen-maps") !== -1
          ? "navbar-absolute fixed-top"
          : "navbar-absolute fixed-top " +
            (color === "transparent" ? "navbar-transparent " : "")
      }>
      <Container fluid>
        <div className="navbar-wrapper">
          <div className="navbar-toggle">
            <button
              type="button"
              ref={sidebarToggle}
              className="navbar-toggler"
              onClick={() => openSidebar()}
            >
              <span className="navbar-toggler-bar bar1" />
              <span className="navbar-toggler-bar bar2" />
              <span className="navbar-toggler-bar bar3" />
            </button>
          </div>
          <NavbarBrand href="/">{getBrand()}</NavbarBrand>
        </div>
        <NavbarToggler onClick={toggle}>
          <span className="navbar-toggler-bar navbar-kebab" />
          <span className="navbar-toggler-bar navbar-kebab" />
          <span className="navbar-toggler-bar navbar-kebab" />
        </NavbarToggler>
        <Collapse isOpen={isOpen} navbar className="justify-content-end">
          {/* <form>
            <InputGroup className="no-border">
              <Input placeholder="Search..." />
              <InputGroupAddon addonType="append">
                <InputGroupText>
                  <i className="nc-icon nc-zoom-split" />
                </InputGroupText>
              </InputGroupAddon>
            </InputGroup>
          </form> */}
          <Nav navbar> 
          <Dropdown
              nav
              isOpen={dropdownOpen}
              toggle={(e) => dropdownToggle(e)}
            >
              <DropdownToggle caret nav>
                <i className="nc-icon nc-circle-10" />
                <p>
                  {userinfo ? (
                    <span className="nav-link">{userinfo}</span>
                  ) : (
                    <span>Account</span>
                  )}
                </p>
              </DropdownToggle>
              <DropdownMenu right>
                {/* {userinfo ? ( */}
                  <DropdownItem tag="a" onClick={handleLogout}>
                    Logout
                  </DropdownItem>
                {/* ) : (
                  <DropdownItem tag={Link} to="http://localhost:3000/login/login">
                    Login
                  </DropdownItem>
                )} */}
              </DropdownMenu>
            </Dropdown>

          {/*  <Dropdown
              nav
              isOpen={dropdownOpen}
              toggle={(e) => dropdownToggle(e)}
            >
              <DropdownToggle caret nav>
                <i className="nc-icon nc-circle-10" />
                <p>
                  {user ? (
                <span className="nav-link">{user.email}</span>
              ) : (
                <span className="d-lg-none d-md-block">Account</span>
              )}
                </p>
              </DropdownToggle>
              <DropdownMenu right>
                <DropdownItem tag="a">Action</DropdownItem>
                <DropdownItem tag="a">Another Action</DropdownItem>
                <DropdownItem tag="a">Something else here</DropdownItem>
              </DropdownMenu>
            </Dropdown>
            <NavItem>
              <Link to="#pablo" className="nav-link btn-rotate">
                <i className="nc-icon nc-settings-gear-65" />
                <p>
                  <span className="d-lg-none d-md-block">Account</span>
                </p>
              </Link>
              </NavItem> */}
          </Nav> 
        </Collapse>
      </Container>
    </Navbar>
  );
}

export default Header;
