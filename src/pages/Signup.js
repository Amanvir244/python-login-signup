import React, { useState } from "react";
import axios from "axios";
import "./../styles/Signup.css";
import { useNavigate, Link } from "react-router-dom";

function Signup() {
  const [form, setForm] = useState({ email: "", password: "" });
  const navigate = useNavigate();

  const handleChange = (e) =>
    setForm({ ...form, [e.target.name]: e.target.value });

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await axios.post("http://127.0.0.1:8000/signup", form);
      alert("Signup successful! You can now log in.");
      navigate("/");
    } catch (err) {
      alert(err.response?.data?.detail || "Signup failed");
    }
  };

  return (
    <div className="signup-page">
      <div className="signup-container">
        <h1>Signup</h1>
        <form onSubmit={handleSubmit}>
          <div>
            <label>Email</label>
            <input
              type="email"
              name="email"
              placeholder="Enter your email"
              value={form.email}
              onChange={handleChange}
            />
          </div>
          <div>
            <label>Password</label>
            <input
              type="password"
              name="password"
              placeholder="Enter your password"
              value={form.password}
              onChange={handleChange}
            />
          </div>
          <button type="submit">Signup</button>
        </form>
        <span>
          Already have an account? <Link to="/">Login</Link>
        </span>
      </div>
    </div>
  );
}

export default Signup;
