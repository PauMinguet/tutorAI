import NavBar1 from "@/app/components/navbar1";
import { UserProfile } from "@clerk/nextjs";

const UserProfilePage = () => (
  <>
    <NavBar1 />
    <UserProfile path="/user-profile" routing="path" />
  </>
);

export default UserProfilePage;
