import React from "react";
import "./about.css";
import { FaFacebook, FaInstagram, FaPhoneAlt, FaEnvelope } from "react-icons/fa";

function About() {
  return (
    <div className="about-page">
      {/* Who We Are Section */}
      <section className="section who-we-are">
        <div className="section-header">
          <h2>Who we are</h2>
        </div>
        <div className="who-content">
          <div className="text-box">
            <p>
              Mzanzi Market, established in 2025, is an online community with a
              love for South Africa’s flourishing market culture.
            </p>
          </div>
          <div className="image-box">
            <img
              src="https://images.unsplash.com/photo-1506744038136-46273834b3fb?auto=format&fit=crop&w=800&q=80"
              alt="Market scene"
            />
          </div>
        </div>
      </section>

      {/* Our Goals Section */}
      <section className="section our-goals">
        <h2>Our goals</h2>
        <div className="goals-container">
          <div className="goal-card">
            <img
              src="https://images.unsplash.com/photo-1581090700227-1e37b190418e?auto=format&fit=crop&w=600&q=80"
              alt="Sustainability"
              className="goal-image"
            />
            <p>Sustainability</p>
          </div>
          <div className="goal-card">
            <img
              src="https://images.unsplash.com/photo-1500530855697-b586d89ba3ee?auto=format&fit=crop&w=600&q=80"
              alt="Community"
              className="goal-image"
            />
            <p>Community</p>
          </div>
          <div className="goal-card">
            <img
              src="https://images.unsplash.com/photo-1522202195463-021b5a90862e?auto=format&fit=crop&w=600&q=80"
              alt="Innovation"
              className="goal-image"
            />
            <p>Innovation</p>
          </div>
        </div>
      </section>

      {/* Our Story Section */}
      <section className="section our-story">
        <div className="story-container">
          <div className="story-image">
            <img
              src="https://images.unsplash.com/photo-1593113598332-cd6c3c516bfd?auto=format&fit=crop&w=800&q=80"
              alt="Market stall"
            />
          </div>
          <div className="story-text">
            <h2>Our story</h2>
            <p>
              Mzanzi Market began with the vision of connecting local artisans,
              farmers, and small businesses through an online platform that
              celebrates authenticity, sustainability, and cultural vibrance.
            </p>
          </div>
        </div>
      </section>

      {/* Contact Section */}
      <section className="section contact-us">
        <h2>Contact us</h2>
        <div className="contact-container">
          <div className="contact-info">
            <p><FaFacebook /> Facebook: @MzanziMarket</p>
            <p><FaInstagram /> Instagram: @mzanzi_market</p>
            <p><FaPhoneAlt /> Cell: +27 82 123 4567</p>
            <p><FaEnvelope /> Email: info@mzanzimarket.co.za</p>
          </div>
          <div className="contact-image">
            <img
              src="https://images.unsplash.com/photo-1556761175-4b46a572b786?auto=format&fit=crop&w=800&q=80"
              alt="Contact banner"
            />
          </div>
        </div>
      </section>
    </div>
  );
}

export default About;
