import LoginBar from "@/app/components/loginnav";
import { SignIn } from "@clerk/nextjs";
import "../../globals.css";


export default function Page() {
  return (
    <div>
      <LoginBar />
      <div className="min-h-screen bg-gray-900 text-white flex flex-col items-center">
        <div className="mt-10">
          <SignIn />
        </div>
      </div>
    </div>
  );
}