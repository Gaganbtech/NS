# Theoretical Background
## Post-Quantum Cryptography for Secure Network Communication

This document provides the cryptographic and theoretical foundation for understanding post-quantum cryptography and its application in secure network communication.

---

## Table of Contents

1. [Introduction](#introduction)
2. [Classical Cryptography](#classical-cryptography)
3. [The Quantum Threat](#the-quantum-threat)
4. [Post-Quantum Cryptography](#post-quantum-cryptography)
5. [CRYSTALS-Kyber (MLKEM)](#crystals-kyber-mlkem)
6. [Hybrid Cryptography](#hybrid-cryptography)
7. [TLS Protocol](#tls-protocol)
8. [Migration Strategy](#migration-strategy)
9. [Conclusion](#conclusion)

---

## Introduction

### The Problem

Modern secure communication relies on public-key cryptography, primarily RSA and Elliptic Curve Cryptography (ECC). These algorithms are secure against classical computers but vulnerable to quantum computers running Shor's algorithm.

### The Timeline

- **1994:** Peter Shor develops quantum algorithm to break RSA
- **2016:** NIST begins post-quantum cryptography standardization
- **2022:** NIST selects finalists (Kyber, Dilithium, SPHINCS+, Falcon)
- **2024:** NIST publishes FIPS 203 (MLKEM/Kyber) standard
- **2030-2035:** Estimated arrival of cryptographically relevant quantum computers
- **2035:** NSA mandates full PQC migration

### The Solution

Post-quantum cryptography provides algorithms resistant to both classical and quantum attacks, enabling secure communication in the quantum era.

---

## Classical Cryptography

### RSA (Rivest-Shamir-Adleman)

**Invented:** 1977  
**Security Basis:** Integer factorization problem

#### How RSA Works

1. **Key Generation:**
   - Select two large primes: p, q
   - Compute n = p × q
   - Compute φ(n) = (p-1)(q-1)
   - Choose e such that gcd(e, φ(n)) = 1
   - Compute d such that e × d ≡ 1 (mod φ(n))
   - Public key: (n, e)
   - Private key: (n, d)

2. **Encryption:**
   - Ciphertext: C = M^e mod n

3. **Decryption:**
   - Plaintext: M = C^d mod n

#### Security

**Classical Security:**
- Best known algorithm: General Number Field Sieve (GNFS)
- Complexity: O(exp((64/9 × ln n)^(1/3) × (ln ln n)^(2/3)))
- RSA-2048: ~2^112 classical security

**Quantum Vulnerability:**
- Shor's algorithm: O((log n)^3)
- RSA-2048: Breakable in hours on large quantum computer

### Elliptic Curve Cryptography (ECC)

**Invented:** 1985 (Koblitz, Miller)  
**Security Basis:** Elliptic Curve Discrete Logarithm Problem (ECDLP)

#### How ECC Works

1. **Curve Definition:**
   - y² = x³ + ax + b (mod p)
   - Base point G of order n

2. **Key Generation:**
   - Private key: d (random integer)
   - Public key: Q = d × G

3. **ECDH Key Exchange:**
   - Alice: private dA, public QA = dA × G
   - Bob: private dB, public QB = dB × G
   - Shared secret: S = dA × QB = dB × QA

#### Security

**Classical Security:**
- Best known algorithm: Pollard's rho
- Complexity: O(√n)
- P-256: ~2^128 classical security

**Quantum Vulnerability:**
- Shor's algorithm applies to ECDLP
- P-256: Breakable on quantum computer

---

## The Quantum Threat

### Quantum Computing Basics

**Qubit:** Quantum bit, can be in superposition of |0⟩ and |1⟩

**Quantum Gates:** Unitary operations on qubits

**Quantum Algorithms:**
- Shor's Algorithm (1994): Factors integers, solves discrete log
- Grover's Algorithm (1996): Searches unstructured data

### Shor's Algorithm

**Purpose:** Factor integers and solve discrete logarithm

**Complexity:**
- Classical: O(exp(n^(1/3)))
- Quantum: O(n³)

**Impact:**
- Breaks RSA
- Breaks ECC
- Breaks Diffie-Hellman
- Breaks DSA/ECDSA

**Requirements:**
- ~4000 logical qubits for RSA-2048
- Error correction (physical qubits: ~1 million)
- Coherence time: hours

### Current Quantum Computers

| System | Qubits | Error Rate | Status |
|--------|--------|------------|--------|
| IBM Condor | 1,121 | ~0.1% | 2023 |
| Google Willow | 105 | ~0.001% | 2024 |
| IonQ Forte | 32 | ~0.0001% | 2024 |

**Gap to Cryptographic Relevance:**
- Need: 4,000+ logical qubits
- Current: ~1,000 physical qubits
- Estimate: 2030-2035 for cryptographic threat

### "Harvest Now, Decrypt Later"

**Threat:** Adversaries capture encrypted data today, decrypt when quantum computers available

**Impact:**
- Long-term sensitive data at risk
- Government communications
- Healthcare records
- Financial transactions
- Intellectual property

**Urgency:** Must migrate to PQC before quantum computers arrive

---

## Post-Quantum Cryptography

### NIST Standardization Process

**Timeline:**
- 2016: Call for proposals (82 submissions)
- 2019: Round 2 (26 candidates)
- 2020: Round 3 (7 finalists)
- 2022: Winners announced
- 2024: FIPS standards published

**Selected Algorithms:**
1. **MLKEM (Kyber)** - Key Encapsulation Mechanism
2. **ML-DSA (Dilithium)** - Digital Signatures
3. **SLH-DSA (SPHINCS+)** - Stateless Hash-based Signatures
4. **FN-DSA (Falcon)** - Compact Signatures

### Mathematical Foundations

#### 1. Lattice-Based Cryptography

**Hard Problem:** Learning With Errors (LWE)

**Definition:**
- Given: (A, b = As + e) where s is secret, e is small error
- Find: s

**Security:**
- No known quantum algorithm
- Reduction to worst-case lattice problems
- Extensively studied (20+ years)

**Advantages:**
- Fast operations
- Simple implementation
- Strong security proofs

**Disadvantages:**
- Larger key sizes
- Ciphertext expansion

#### 2. Hash-Based Cryptography

**Hard Problem:** Collision resistance of hash functions

**Security:**
- Based on hash function security
- Quantum-resistant (Grover only gives √n speedup)
- Provably secure

**Advantages:**
- Well-understood security
- Conservative choice
- No mathematical assumptions

**Disadvantages:**
- Large signatures
- Stateful (for some variants)

#### 3. Code-Based Cryptography

**Hard Problem:** Decoding random linear codes

**Security:**
- No known quantum algorithm
- 40+ years of analysis

**Advantages:**
- Fast decryption
- Mature theory

**Disadvantages:**
- Very large keys
- Limited adoption

#### 4. Multivariate Cryptography

**Hard Problem:** Solving multivariate polynomial equations

**Security:**
- NP-hard problem
- Quantum-resistant

**Advantages:**
- Fast signatures
- Small signatures

**Disadvantages:**
- Large keys
- Some broken variants

---

## CRYSTALS-Kyber (MLKEM)

### Overview

**Full Name:** Module-Lattice-based Key Encapsulation Mechanism  
**Standardized:** FIPS 203 (2024)  
**Type:** Key Encapsulation Mechanism (KEM)  
**Security:** Lattice-based (Module-LWE)

### Security Levels

| Parameter Set | Security Level | Public Key | Ciphertext | Shared Secret |
|---------------|----------------|------------|------------|---------------|
| MLKEM512 | ~AES-128 | 800 bytes | 768 bytes | 32 bytes |
| MLKEM768 | ~AES-192 | 1184 bytes | 1088 bytes | 32 bytes |
| MLKEM1024 | ~AES-256 | 1568 bytes | 1568 bytes | 32 bytes |

**Recommended:** MLKEM768 (balance of security and performance)

### Algorithm Description

#### Key Generation

```
Input: None
Output: (pk, sk) - public and secret keys

1. Generate random seed ρ
2. Generate matrix A from ρ
3. Generate secret vector s (small coefficients)
4. Generate error vector e (small coefficients)
5. Compute t = As + e
6. pk = (ρ, t)
7. sk = s
```

#### Encapsulation

```
Input: pk - public key
Output: (ct, ss) - ciphertext and shared secret

1. Generate random message m
2. Derive randomness r from m
3. Generate small vectors r', e1, e2
4. Compute u = A^T r' + e1
5. Compute v = t^T r' + e2 + encode(m)
6. ct = (u, v)
7. ss = KDF(m)
```

#### Decapsulation

```
Input: ct, sk - ciphertext and secret key
Output: ss - shared secret

1. Parse ct = (u, v)
2. Compute m' = decode(v - s^T u)
3. Re-encapsulate to verify
4. ss = KDF(m')
```

### Security Analysis

**Classical Security:**
- Core-SVP hardness: 2^154 for MLKEM768
- Resistant to all known classical attacks

**Quantum Security:**
- Grover's algorithm: √n speedup
- Effective security: 2^128 for MLKEM768
- No known better quantum algorithm

**Attacks Considered:**
- Primal attack
- Dual attack
- Hybrid attack
- Enumeration attack
- All require exponential time

### Performance

**MLKEM768 Benchmarks (Intel i7):**
- Key generation: 0.05 ms
- Encapsulation: 0.07 ms
- Decapsulation: 0.09 ms

**Comparison to RSA-2048:**
- 50x faster key generation
- 10x faster encryption
- 50x faster decryption

**Network Overhead:**
- Additional ~2KB per TLS handshake
- Negligible for most applications
- Acceptable for IoT with optimization

---

## Hybrid Cryptography

### Motivation

**Why Hybrid?**

1. **Conservative Security:** If PQC has undiscovered weakness, classical crypto still protects
2. **Compliance:** Some regulations require classical algorithms
3. **Gradual Migration:** Smooth transition without breaking existing systems
4. **Defense-in-Depth:** Both algorithms must be broken

### Hybrid Key Exchange

**Approach:** Combine classical ECDH with PQC KEM

```
Client                                  Server
------                                  ------

1. Generate ECDH keypair (dC, QC)
2. Generate Kyber keypair (skC, pkC)
                ClientHello
                QC, pkC
                -------->
                                3. Generate ECDH keypair (dS, QS)
                                4. Compute ECDH shared: S1 = dS × QC
                                5. Encapsulate with pkC: (ct, S2)
                ServerHello
                QS, ct
                <--------
6. Compute ECDH shared: S1 = dC × QS
7. Decapsulate ct: S2
8. Combine: K = KDF(S1 || S2)
                                9. Combine: K = KDF(S1 || S2)
```

**Security:**
- Attacker must break BOTH ECDH AND Kyber
- If either is secure, communication is secure
- Provides quantum resistance via Kyber
- Provides classical security via ECDH

### Standardization

**IETF Drafts:**
- draft-ietf-tls-hybrid-design
- draft-ietf-tls-hybrid-kem

**Implementations:**
- Google Chrome (X25519Kyber768)
- Cloudflare
- AWS
- OpenSSL with OQS

**Naming Convention:**
- X25519MLKEM768 (ECDH + PQC)
- P256MLKEM768 (NIST curve + PQC)

---

## TLS Protocol

### TLS 1.3 Handshake

```
Client                                  Server

ClientHello
  + key_share (ECDH/Kyber)
  + supported_groups
                -------->
                                ServerHello
                                  + key_share
                                {EncryptedExtensions}
                                {Certificate}
                                {CertificateVerify}
                                {Finished}
                <--------
{Finished}
                -------->
[Application Data]      <------->      [Application Data]
```

**Key Points:**
- 1-RTT handshake (vs 2-RTT in TLS 1.2)
- Forward secrecy mandatory
- Encrypted certificates
- No RSA key transport

### Cipher Suites

**TLS 1.3 Format:**
```
TLS_AEAD_HASH
```

**Examples:**
- TLS_AES_256_GCM_SHA384
- TLS_CHACHA20_POLY1305_SHA256

**Key Exchange Separate:**
- Negotiated via supported_groups extension
- RSA, ECDH, or PQC KEM

### PQC Integration

**Supported Groups Extension:**
```
supported_groups:
  - x25519 (classical ECDH)
  - secp256r1 (classical ECDH)
  - mlkem768 (PQC KEM)
  - x25519mlkem768 (Hybrid)
```

**Key Share Extension:**
```
key_share:
  - group: x25519mlkem768
  - data: <ECDH public key> || <Kyber public key>
```

---

## Migration Strategy

### Phase 1: Assessment (Now - 2025)

**Actions:**
1. Inventory cryptographic systems
2. Identify quantum-vulnerable components
3. Assess PQC readiness
4. Plan migration timeline

**Systems to Assess:**
- TLS/HTTPS
- VPNs (IPsec, OpenVPN)
- SSH
- PKI/Certificate Authorities
- Email encryption (S/MIME, PGP)
- Code signing
- IoT devices

### Phase 2: Testing (2025-2027)

**Actions:**
1. Deploy PQC in test environments
2. Measure performance impact
3. Test interoperability
4. Train staff
5. Update policies

**Hybrid Deployment:**
- Enable hybrid cipher suites
- Monitor for issues
- Gradual rollout

### Phase 3: Production (2027-2030)

**Actions:**
1. Deploy hybrid mode in production
2. Monitor and optimize
3. Update all systems
4. Maintain classical support

**Priority Order:**
1. High-value targets (government, finance)
2. Long-term sensitive data
3. Public-facing services
4. Internal systems

### Phase 4: Pure PQC (2030-2035)

**Actions:**
1. Transition to pure PQC
2. Deprecate classical-only systems
3. Full quantum resistance

**Timeline Drivers:**
- Quantum computer development
- Regulatory requirements
- Industry standards

---

## Conclusion

### Key Takeaways

1. **Quantum Threat is Real:** Quantum computers will break RSA and ECC
2. **Timeline is Urgent:** 2030-2035 estimated, "harvest now, decrypt later" already happening
3. **PQC is Ready:** NIST-standardized algorithms available now
4. **Hybrid is Recommended:** Provides security during transition
5. **Migration is Complex:** Requires planning, testing, and gradual deployment

### Future Directions

**Research Areas:**
- More efficient PQC algorithms
- Hardware acceleration
- Formal verification
- Quantum-resistant protocols beyond TLS

**Industry Trends:**
- Widespread hybrid deployment
- PQC in hardware (TPMs, HSMs)
- Quantum-safe PKI
- PQC for IoT

### Final Thoughts

Post-quantum cryptography is not just a theoretical concern—it's a practical necessity. Organizations must begin migration now to ensure long-term security. This project demonstrates that PQC is deployable today using real tools and standards.

**The quantum era is coming. Are you ready?**

---

## References

1. NIST. (2024). FIPS 203: Module-Lattice-Based Key-Encapsulation Mechanism Standard.
2. Shor, P. W. (1994). Algorithms for quantum computation: discrete logarithms and factoring.
3. Alagic, G., et al. (2022). Status Report on the Third Round of the NIST Post-Quantum Cryptography Standardization Process.
4. Bos, J., et al. (2018). CRYSTALS-Kyber: A CCA-Secure Module-Lattice-Based KEM.
5. Rescorla, E. (2018). RFC 8446: The Transport Layer Security (TLS) Protocol Version 1.3.
6. Stebila, D., & Mosca, M. (2016). Post-quantum key exchange for the Internet and the Open Quantum Safe project.
7. NSA. (2022). Announcing the Commercial National Security Algorithm Suite 2.0.
8. Mosca, M. (2018). Cybersecurity in an Era with Quantum Computers.

---

**Document Version:** 1.0  
**Last Updated:** April 2026  
**Author:** Network Security Project Team
