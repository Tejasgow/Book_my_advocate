import { useState } from "react";
import { FaEnvelope, FaLock, FaEye, FaEyeSlash } from "react-icons/fa";
import { Link } from "react-router-dom";
import "./Auth.css";

export default function Login() {
  const [form, setForm] = useState({
    email: "",
    password: "",
  });

  const [showPassword, setShowPassword] = useState(false);
  const [error, setError] = useState("");

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
    setError("");
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    if (!form.email || !form.password) {
      setError("Email and password are required");
      return;
    }

    console.log("Login Data:", form);
  };

  return (
    <div className="auth-page">
      <div className="auth-card card border-0 p-4">
        <h3 className="text-center mb-1 auth-title">
          Book My Advocate
        </h3>
        <p className="text-center auth-subtitle mb-4">
          Login to your legal account
        </p>

        {error && (
          <div className="alert alert-danger text-center">{error}</div>
        )}

        <form onSubmit={handleSubmit}>
          {/* Email */}
          <div className="mb-3">
            <label className="form-label">Email Address</label>
            <div className="input-group">
              <span className="input-group-text">
                <FaEnvelope />
              </span>
              <input
                type="email"
                name="email"
                className="form-control"
                placeholder="Enter email"
                value={form.email}
                onChange={handleChange}
              />
            </div>
          </div>

          {/* Password */}
          <div className="mb-3">
            <label className="form-label">Password</label>
            <div className="input-group">
              <span className="input-group-text">
                <FaLock />
              </span>
              <input
                type={showPassword ? "text" : "password"}
                name="password"
                className="form-control"
                placeholder="Enter password"
                value={form.password}
                onChange={handleChange}
              />
              <span
                className="input-group-text"
                style={{ cursor: "pointer" }}
                onClick={() => setShowPassword(!showPassword)}
              >
                {showPassword ? <FaEyeSlash /> : <FaEye />}
              </span>
            </div>
          </div>

          <div className="d-flex justify-content-end mb-3">
            <Link to="/forgot-password" className="auth-link text-decoration-none">
              Forgot password?
            </Link>
          </div>

          <button className="btn btn-primary w-100">
            Login
          </button>
        </form>

        <div className="text-center mt-3">
          <span className="text-muted">Don’t have an account?</span>{" "}
          <Link to="/register" className="auth-link text-decoration-none">
            Register
          </Link>
        </div>
      </div>
    </div>
  );
}
