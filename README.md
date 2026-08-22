# TARGET-STABILITY

**Companion software for:** *Variant-level concordance can overstate exact peptide–HLA shortlist reproducibility: a 63-condition HCC1395 audit*

This public record supports a computational reproducibility audit of neoantigen-shortlist selection in the HCC1395/HCC1395BL SEQC2 reference system. Across 63 provenance-defined analytical conditions, it evaluates agreement at variant, peptide, and exact variant–peptide–HLA resolution.

> **Research boundary:** This is a computational methods and reproducibility audit. It does not establish peptide presentation, immunogenicity, vaccine-target suitability, efficacy, safety, treatment benefit, or clinical utility. No biological candidate is nominated. The HG008 holdout was not accessed.

## Verified release

The full reproducibility archive is attached to release **v1.0.0** together with its SHA-256 sidecar.

- 60/60 tests passed in a clean Python 3.12 environment.
- Fail-closed preflight passed before and after the test suite.
- Internal manifest verified 123/123 bundled files.
- Journal-support archive SHA-256: `a83536d1d66690530203dfd590543831db765f497fabe2206b6739124d2c62f7`.
- Machine-local user paths, secrets, third-party payloads, and the HG008 holdout are absent.

## Reproduce

```bash
python -m venv .venv
# Windows: .venv\Scripts\activate
# macOS/Linux: source .venv/bin/activate
python -m pip install -r requirements-analysis-lock.txt
python -m target_stability.cli preflight --allow-missing-dev
python -m unittest discover -s tests -v
python -m target_stability.cli preflight --allow-missing-dev
```

The release archive contains the code, frozen configuration, test suite, derived TSV/JSON artifacts, reports, manifests, and deterministic figure scripts. Full upstream rescoring additionally requires the checksum-pinned public inputs and MHCflurry model archive documented inside `THIRD_PARTY_SOURCES.md`.

## License

Author-generated source code is MIT. Author-generated documentation, figures, configuration, and derived TSV/JSON artifacts are CC BY 4.0. Third-party materials are excluded and remain governed by their providers' terms.

## Author

Byungwoong Yoo — Independent Researcher, Seoul, Republic of Korea  
ORCID: https://orcid.org/0009-0002-1797-3100  
Scholarly contact: yoonge3@gmail.com
