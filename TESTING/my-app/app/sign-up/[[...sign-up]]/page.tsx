import LoginBar from "@/app/components/loginnav";
import { SignUp } from "@clerk/nextjs";
import "../../globals.css";


export default function Page() {
  return (
    <div>
      <LoginBar />
      <div className="min-h-screen bg-gray-900 text-white flex flex-col items-center">
        <div className="mt-10">
          <SignUp />
        </div>
      </div>
    </div>
  );
}