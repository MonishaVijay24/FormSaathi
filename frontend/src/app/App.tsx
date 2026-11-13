import { BrowserRouter, Navigate, Route, Routes, useLocation } from "react-router-dom";
import type { ReactNode } from "react";
import { ApplicationProvider } from "../context/ApplicationContext";
import { Layout } from "../components/Layout";
import Landing from "../pages/Landing";
import Profile from "../pages/Profile";
import Applications from "../pages/Applications";
import UploadForm from "../pages/UploadForm";
import Extraction from "../pages/Extraction";
import Assistant from "../pages/Assistant";
import Documents from "../pages/Documents";
import Validation from "../pages/Validation";
import Preview from "../pages/Preview";
import Dashboard from "../pages/Dashboard";
import { useApplication } from "../context/ApplicationContext";

function FlowGuard({ minimum, children }: { minimum: "form" | "fields" | "answers" | "validation"; children: ReactNode }) {
  const { state } = useApplication();
  const location = useLocation();
  const allowed = minimum === "form"
    ? Boolean(state.selectedForm)
    : minimum === "fields"
      ? state.fields.length > 0
      : minimum === "answers"
        ? state.fields.length > 0 && Object.keys(state.answers).length > 0
        : state.validationIssues.length > 0;
  if (allowed) return <>{children}</>;
  const destination = minimum === "form" ? "/forms" : minimum === "fields" ? "/forms/upload" : minimum === "answers" ? "/answer" : "/verify";
  return <Navigate to={destination} state={{ from: location.pathname }} replace />;
}

export default function App() {
  return (
    <ApplicationProvider>
      <BrowserRouter>
        <Routes>
          <Route path="/" element={<Landing />} />
          <Route element={<Layout><Outlet /></Layout>}>
            <Route path="/dashboard" element={<Dashboard />} />
            <Route path="/profile" element={<Profile />} />
            <Route path="/forms" element={<Applications />} />
            <Route path="/upload" element={<FlowGuard minimum="form"><UploadForm /></FlowGuard>} />
            <Route path="/forms/upload" element={<FlowGuard minimum="form"><UploadForm /></FlowGuard>} />
            <Route path="/extraction" element={<FlowGuard minimum="fields"><Extraction /></FlowGuard>} />
            <Route path="/forms/review" element={<FlowGuard minimum="fields"><Extraction /></FlowGuard>} />
            <Route path="/answer" element={<FlowGuard minimum="fields"><Assistant /></FlowGuard>} />
            <Route path="/assistant" element={<FlowGuard minimum="fields"><Assistant /></FlowGuard>} />
            <Route path="/documents" element={<FlowGuard minimum="answers"><Documents /></FlowGuard>} />
            <Route path="/validation" element={<FlowGuard minimum="answers"><Validation /></FlowGuard>} />
            <Route path="/verify" element={<FlowGuard minimum="answers"><Validation /></FlowGuard>} />
            <Route path="/preview" element={<FlowGuard minimum="validation"><Preview /></FlowGuard>} />
          </Route>
          <Route path="*" element={<Navigate to="/" />} />
        </Routes>
      </BrowserRouter>
    </ApplicationProvider>
  );
}

// Need to import Outlet from react-router-dom
import { Outlet } from "react-router-dom";
