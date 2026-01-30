import { useState } from "react";
import { FaUser, FaEnvelope, FaLock, FaPhone } from "react-icons/fa";
import { Link } from "react-router-dom";
import "./Auth.css";

export default function Register() {
  const [form, setForm] = useState({
    name: "",
    email: "",
    mobile: "",
    role: "",
    password: "",
    confirm_password: "",
  });

  const [error, setError] = useState("");

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
    setError("");
  };

  const handleSubmit = (e) => {
    e.preventDefault();

    if (
      !form.name ||
      !form.email ||
      !form.mobile ||
      !form.role ||
      !form.password ||
      !form.confirm_password
    ) {
      setError("All fields are required");
      return;
    }

    if (form.password !== form.confirm_password) {
      setError("Passwords do not match");
      return;
    }

    console.log("Register Data:", form);
  };

  return (
    <div className="auth-page">
      <div className="auth-card">
        <h3 className="auth-title text-center">Book My Advocate</h3>
        <p className="auth-subtitle text-center">Create your account</p>

        {error && (
          <div className="alert alert-danger py-1 text-center small">
            {error}
          </div>
        )}

        <form onSubmit={handleSubmit}>
          {/* Full Name */}
          <div className="mb-3">
            <label className="form-label">Full Name</label>
            <div className="input-group">
              <span className="input-group-text">
                <FaUser />
              </span>
              <input
                type="text"
                name="name"
                className="form-control"
                placeholder="Enter full name"
                value={form.name}
                onChange={handleChange}
              />
            </div>
          </div>

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

          {/* Mobile */}
          <div className="mb-3">
            <label className="form-label">Mobile Number</label>
            <div className="input-group">
              <span className="input-group-text">
                <FaPhone />
              </span>
              <input
                type="tel"
                name="mobile"
                className="form-control"
                placeholder="Enter mobile number"
                value={form.mobile}
                onChange={handleChange}
              />
            </div>
          </div>

          {/* Role */}
          <div className="mb-3">
            <label className="form-label">Register As</label>
            <select
              name="role"
              className="form-select"
              value={form.role}
              onChange={handleChange}
            >
              <option value="">Select Role</option>
              <option value="client">Client</option>
              <option value="advocate">Advocate</option>
            </select>
          </div>

          {/* Password */}
          <div className="mb-3">
            <label className="form-label">Password</label>
            <div className="input-group">
              <span className="input-group-text">
                <FaLock />
              </span>
              <input
                type="password"
                name="password"
                className="form-control"
                placeholder="Enter password"
                value={form.password}
                onChange={handleChange}
              />
            </div>
          </div>

          {/* Confirm Password */}
          <div className="mb-3">
            <label className="form-label">Confirm Password</label>
            <div className="input-group">
              <span className="input-group-text">
                <FaLock />
              </span>
              <input
                type="password"
                name="confirm_password"
                className="form-control"
                placeholder="Confirm password"
                value={form.confirm_password}
                onChange={handleChange}
              />
            </div>
          </div>

          <button className="btn btn-primary w-100 fw-semibold">
            Register
          </button>
        </form>

        <div className="text-center mt-3">
          <span className="text-muted">Already have an account?</span>{" "}
          <Link to="/login" className="auth-link">
            Login
          </Link>
        </div>
      </div>
    </div>
  );
}
