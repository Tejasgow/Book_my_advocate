import { useState } from "react";
import { FaUser, FaEnvelope, FaLock, FaPhone } from "react-icons/fa";
import { Link } from "react-router-dom";
import "./AuthSlider.css";

export default function AuthSlider() {
  const [isRegister, setIsRegister] = useState(false);

  return (
    <div className="auth-slider-page">
      <div className={`auth-slider-card ${isRegister ? "active" : ""}`}>
        
        {/* LOGIN */}
        <div className="auth-form login-form">
          <h3>Welcome Back</h3>
          <p className="text-muted">Login to your account</p>

          <div className="mb-3">
            <div className="input-group">
              <span className="input-group-text"><FaEnvelope /></span>
              <input type="email" className="form-control" placeholder="Email" />
            </div>
          </div>

          <div className="mb-3">
            <div className="input-group">
              <span className="input-group-text"><FaLock /></span>
              <input type="password" className="form-control" placeholder="Password" />
            </div>
          </div>

          <button className="btn btn-primary w-100">Login</button>

          <p className="switch-text">
            Don’t have an account?{" "}
            <span onClick={() => setIsRegister(true)}>Register</span>
          </p>
        </div>

        {/* REGISTER */}
        <div className="auth-form register-form">
          <h3>Create Account</h3>
          <p className="text-muted">Join Book My Advocate</p>

          <div className="mb-2">
            <div className="input-group">
              <span className="input-group-text"><FaUser /></span>
              <input type="text" className="form-control" placeholder="Full Name" />
            </div>
          </div>

          <div className="mb-2">
            <div className="input-group">
              <span className="input-group-text"><FaEnvelope /></span>
              <input type="email" className="form-control" placeholder="Email" />
            </div>
          </div>

          <div className="mb-2">
            <div className="input-group">
              <span className="input-group-text"><FaPhone /></span>
              <input type="tel" className="form-control" placeholder="Mobile" />
            </div>
          </div>

          <div className="mb-2">
            <select className="form-select">
              <option>Select Role</option>
              <option>Client</option>
              <option>Advocate</option>
            </select>
          </div>

          <div className="mb-2">
            <div className="input-group">
              <span className="input-group-text"><FaLock /></span>
              <input type="password" className="form-control" placeholder="Password" />
            </div>
          </div>

          <button className="btn btn-primary w-100">Register</button>

          <p className="switch-text">
            Already have an account?{" "}
            <span onClick={() => setIsRegister(false)}>Login</span>
          </p>
        </div>

      </div>
    </div>
  );
}
