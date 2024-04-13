import "../globals.css";
import NavBar1 from '../components/navbar1';
import { auth, currentUser } from "@clerk/nextjs";

export default async function Home() {

  const {userId} = auth();
  console.log(userId);

  const user = await currentUser();


  return (
    <div className="min-h-screen bg-gray-900 text-white flex flex-col">
      <NavBar1/>
      <main className="flex flex-col items-center justify-center py-2 text-center flex-grow">
        <div className="z-10 max-w-5xl w-full p-6 bg-gray-800 rounded-xl shadow-md space-y-4">
          <h1 className="text-6xl font-extrabold text-purple-600 mb-4">
            HOME
          </h1>

          <p className="text-lg text-red-500 font-medium">
            Lots more features coming soon!
          </p>
        </div>
      </main>
      <footer className="bg-gray-800 p-4 text-center text-sm">
        <p>&copy; 2024 tutorAI. All rights reserved.</p>
        <p>123 Main St, Anytown, USA</p>
        <p>Email: info@tutorai.com</p>
      </footer>
    </div>
  );
}

