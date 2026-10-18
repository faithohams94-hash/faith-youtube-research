// ---------- extra traced courses ----------
Object.assign(S.greater_occipital_n, { steps: [
  [466, 470, "Arises as the medial branch of the dorsal ramus of C2, emerging below the inferior oblique and curving up around it.", []],
  [473, 410, "Ascends across the suboccipital triangle on semispinalis capitis, then PIERCES semispinalis capitis.", []],
  [471, 355, "PIERCES the trapezius aponeurosis about 2 cm below and lateral to the external occipital protuberance and meets the occipital artery.", ["occipital_a"]],
  [445, 180, "Climbs the back of the scalp in layer C to supply the skin up to the vertex.", ["d_go", "occipitalis"]]] });
Object.assign(S.great_auricular_n, { steps: [
  [410, 560, "Emerges at the nerve point (Erb's point): the midpoint of the posterior border of sternocleidomastoid (C2, C3).", ["scm"]],
  [398, 500, "Ascends obliquely across the superficial surface of SCM, deep to platysma, parallel to and behind the external jugular vein.", ["scm", "platysma", "ejv"]],
  [389, 420, "Divides near the parotid: anterior branch to the skin over the parotid and angle of the mandible, posterior branch to the ear lobule.", ["parotid", "d_c23"]]] });
Object.assign(S.lesser_occipital_n, { steps: [
  [420, 522, "Emerges at the nerve point, hooking around the spinal accessory nerve (C2).", ["scm"]],
  [436, 420, "Ascends along the posterior border of sternocleidomastoid.", ["scm"]],
  [452, 300, "Pierces the deep fascia near the skull to supply the scalp behind and above the ear.", ["d_lo"]]] });
Object.assign(S.buccal_n, { steps: [
  [300, 392, "Arises from the anterior division of V3 and passes between the two heads of lateral pterygoid.", []],
  [262, 400, "Runs forward deep to the ramus, the tendon of temporalis and masseter, onto the outer surface of buccinator.", ["masseter", "temporalis"]],
  [214, 415, "Supplies the skin of the cheek; its branches PIERCE buccinator to supply the buccal mucosa and gum. It does not supply the muscle.", ["buccinator"]]] });
Object.assign(S.parotid_duct, { steps: [
  [335, 360, "Leaves the anterior border of the parotid gland.", ["parotid"]],
  [285, 364, "Crosses superficial to masseter a fingerbreadth below the zygomatic arch, with buccal branches of CN VII and the transverse facial artery.", ["masseter", "cn7_buccal", "transverse_facial_a"]],
  [249, 369, "Turns sharply medially around the anterior border of masseter, through the buccal pad of fat.", ["masseter"]],
  [238, 386, "PIERCES buccinator obliquely and opens on a papilla opposite the upper 2nd molar.", ["buccinator"]]] });
Object.assign(S.cn7_marginal, { steps: [
  [346, 404, "Leaves the lower pole of the parotid gland.", ["parotid"]],
  [318, 492, "Runs forward below the angle of the mandible, deep to platysma; it may dip 1–2 cm below the mandible.", ["platysma", "mandible"]],
  [262, 512, "Crosses SUPERFICIAL to the facial artery and vein at the anterior border of masseter: the danger point in submandibular surgery.", ["facial_a", "facial_v", "masseter"]],
  [170, 476, "Supplies depressor anguli oris, depressor labii inferioris and mentalis.", ["dao", "dli", "mentalis"]]] });
Object.assign(S.cn7_buccal, { steps: [
  [346, 402, "Leaves the anterior border of the parotid with the parotid duct.", ["parotid", "parotid_duct"]],
  [262, 393, "Runs forward across masseter alongside the parotid duct.", ["masseter", "parotid_duct"]],
  [165, 416, "Supplies buccinator, orbicularis oris and the muscles of the upper lip and nose.", ["buccinator", "orb_oris", "zyg_major", "lls"]]] });
Object.assign(S.cn7_zygomatic, { steps: [
  [346, 400, "Leaves the upper anterior border of the parotid gland.", ["parotid"]],
  [255, 332, "Crosses the zygomatic bone toward the lateral angle of the eye.", ["zyg_arch"]],
  [205, 304, "Supplies the lower part of orbicularis oculi: essential for eye closure.", ["orb_oculi"]]] });
Object.assign(S.cn7_cervical, { steps: [
  [346, 406, "Leaves the lower pole of the parotid gland.", ["parotid"]],
  [332, 555, "Descends into the neck, deep to platysma, to supply it.", ["platysma"]]] });
Object.assign(S.mental_n, { steps: [
  [176, 470, "Emerges from the mental foramen below the lower 2nd premolar as the terminal branch of the inferior alveolar nerve.", ["f_mental", "inf_alveolar_n"]],
  [120, 448, "Branches pass up deep to depressor labii inferioris to the skin and mucosa of the lower lip.", ["dli", "orb_oris"]]] });
Object.assign(S.ejv, { steps: [
  [372, 485, "Formed just below the parotid by the posterior division of the retromandibular vein and the posterior auricular vein.", ["rmv", "post_auricular_v"]],
  [388, 590, "Runs down obliquely across the superficial surface of SCM, deep to platysma.", ["scm", "platysma"]],
  [403, 700, "PIERCES the investing layer of deep cervical fascia just above the clavicle and ends in the subclavian vein.", []]] });

// ---------- relations at each step: d = deep to, s = superficial to, p = pierces / passes through, w = runs with ----------
// A word that is a structure id becomes a link and lights up on the model; anything in brackets is a note.
const REL = {
  facial_a: [
    { d: ["platysma", "investing fascia"], w: ["lingual_a (may share a linguofacial trunk)"] },
    { d: ["digastric_post", "stylohyoid"], s: ["superior constrictor (tonsil bed)"] },
    { d: ["submand_gland (grooves it, then arches over its upper border)"], w: ["submental_a"] },
    { d: ["platysma", "skin"], s: ["mandible"], w: ["facial_v (just behind)", "cn7_marginal (crosses superficially)"] },
    { d: ["platysma", "risorius", "zyg_major", "zyg_minor"], s: ["buccinator", "lao"] },
    { d: ["zyg_major", "risorius"], s: ["buccinator"], w: ["sup_labial_a", "inf_labial_a (run deep to orb_oris)"] },
    { d: ["llsan"], w: ["lat_nasal_a"] },
    { p: ["llsan (runs in its fibres)"], w: ["angular_v (lateral)", "dorsal_nasal_a (anastomosis)"] }],
  facial_v: [
    { w: ["supratrochlear_v", "supraorbital_v"] },
    { d: ["zyg_major", "zyg_minor"], w: ["facial_a (in front)"] },
    { w: ["deep_facial_v"] },
    { d: ["risorius", "platysma"], s: ["buccinator", "masseter"] },
    { d: ["platysma", "cn7_marginal"], s: ["mandible"], w: ["facial_a (in front)"] },
    { s: ["submand_gland"], w: ["rmv (anterior division)"] }],
  angular_v: [{ w: ["angular_a (medial)"] }, { w: ["sup_ophthalmic_v"] }, {}],
  sta: [
    { w: ["parotid (inside it)", "stv"] },
    { w: ["transverse_facial_a"] },
    { d: ["skin", "auricularis (anterior)"], s: ["zyg_arch (posterior root)"], w: ["stv", "auriculotemporal_n (behind)", "cn7_temporal (in front)"] },
    { d: ["skin (layer C)"], s: ["temporal fascia", "temporalis"], w: ["stv"] },
    { w: ["supraorbital_a", "supratrochlear_a (anastomoses)"] },
    { w: ["occipital_a", "post_auricular_a (anastomoses)"] }],
  occipital_a: [
    { w: ["hypoglossal nerve (hooks round its origin)"] },
    { d: ["digastric_post"], s: ["ica", "ijv", "CN X and XI"] },
    { d: ["scm", "splenius capitis", "longissimus capitis"], s: ["occipital groove of the temporal bone"] },
    { p: ["deep fascia between SCM and trapezius"], w: ["greater_occipital_n (medial)"] },
    { s: ["galea", "occipitalis"], w: ["greater_occipital_n"] }],
  post_auricular_a: [{ w: ["parotid"] }, { w: ["mastoid (between it and the ear cartilage)"] }, { s: ["auricularis (posterior)"] }],
  eca: [
    { d: ["scm (anterior border)", "platysma"], w: ["ica (posterolateral at first)"] },
    {}, {},
    { d: ["digastric_post", "stylohyoid", "hypoglossal nerve"], s: ["styloglossus", "stylopharyngeus", "CN IX (these separate it from the ica)"] },
    { d: ["cn7", "rmv"], p: ["parotid (enters it)"] },
    { d: ["parotid", "cn7", "rmv"] }],
  maxillary_a: [
    { d: ["mandible (medial to its neck)"], s: ["sphenomandibular ligament"] },
    { w: ["inf_alveolar_n", "auriculotemporal_n"] },
    { w: ["lateral pterygoid (superficial or deep to its lower head)"] },
    { p: ["pterygomaxillary fissure"] }],
  supraorbital_a: [{ p: ["supraorbital notch"], w: ["supraorbital_n"] }, { d: ["frontalis"], p: ["frontalis"] }, { s: ["galea"], w: ["sta (anastomosis)"] }],
  supraorbital_n: [{ p: ["supraorbital notch"], w: ["supraorbital_a"] }, { d: ["frontalis"], p: ["frontalis"] }, { s: ["galea"] }],
  infraorbital_n: [
    { p: ["inferior orbital fissure"] },
    { d: ["inferior rectus", "orbital fat (in the orbital floor)"], w: ["infraorbital_a"] },
    { d: ["lls"], s: ["lao"], p: ["infraorbital foramen"] },
    { d: ["orb_oculi", "lls", "zyg_minor"] }],
  auriculotemporal_n: [
    { d: ["lateral pterygoid"], w: ["middle_meningeal_a (its two roots encircle it)"] },
    { d: ["parotid (upper part)"], w: ["mandible (between its neck and the sphenomandibular ligament)"] },
    { s: ["zyg_arch"], w: ["sta (in front)", "stv"] },
    { s: ["temporal fascia"] }],
  cn7: [
    { p: ["f_stylomastoid"], w: ["stylomastoid artery"] },
    { w: ["post_auricular_n", "digastric_post"] },
    { s: ["rmv", "eca"], p: ["parotid (enters its posteromedial surface)"] },
    { w: ["parotid (divides inside it)"] }],
  cn7_temporal: [{ w: ["parotid"] }, { d: ["skin", "superficial temporal fascia"], s: ["zyg_arch"] }, { s: ["frontalis (enters its deep surface)"] }],
  rmv: [{ w: ["parotid (inside it)"] }, { d: ["cn7"], s: ["eca"] }, {}, { w: ["facial_v"] }, { w: ["post_auricular_v"] }],
  stv: [{ w: ["sta"] }, {}, { s: ["zyg_arch"], w: ["sta (in front)", "auriculotemporal_n (behind)"] }, { p: ["parotid (enters it)"], w: ["maxillary_v"] }],
  greater_occipital_n: [
    { w: ["inferior oblique (curves round it)"] },
    { p: ["semispinalis capitis"] },
    { p: ["trapezius (aponeurosis)"], w: ["occipital_a (lateral)"] },
    { s: ["galea", "occipitalis"], w: ["occipital_a"] }],
  great_auricular_n: [{ w: ["scm (posterior border, nerve point)"] }, { d: ["platysma"], s: ["scm"], w: ["ejv (in front)"] }, { w: ["parotid"] }],
  lesser_occipital_n: [{ w: ["spinal accessory nerve (hooks round it)"] }, { w: ["scm (posterior border)"] }, { p: ["deep fascia"] }],
  buccal_n: [{ p: ["lateral pterygoid (between its two heads)"] }, { d: ["masseter", "temporalis (tendon)"] }, { s: ["buccinator"], p: ["buccinator (branches to the mucosa)"] }],
  parotid_duct: [{ w: ["parotid"] }, { s: ["masseter"], w: ["cn7_buccal", "transverse_facial_a (above)"] }, { w: ["buccal pad of fat"] }, { p: ["buccinator"] }],
  cn7_marginal: [{ w: ["parotid"] }, { d: ["platysma"] }, { d: ["platysma"], s: ["facial_a", "facial_v"] }, { s: ["dao", "dli (enters their deep surfaces)"] }],
  cn7_buccal: [{ w: ["parotid_duct"] }, { s: ["masseter"], w: ["parotid_duct"] }, { s: ["buccinator"] }],
  cn7_zygomatic: [{ w: ["parotid"] }, { s: ["zyg_arch"] }, { s: ["orb_oculi (enters its deep surface)"] }],
  cn7_cervical: [{ w: ["parotid"] }, { d: ["platysma"] }],
  mental_n: [{ p: ["f_mental"], w: ["mental_a"] }, { d: ["dli"] }],
  ejv: [{ w: ["rmv", "post_auricular_v"] }, { d: ["platysma"], s: ["scm"], w: ["great_auricular_n (behind)"] }, { p: ["investing layer of deep cervical fascia"] }]
};
const REL_LABEL = { d: "Deep to", s: "Superficial to", p: "Pierces / passes through", w: "Runs with" };
function relParts(str) {
  const m = String(str).match(/^([a-z0-9_]+)(.*)$/);
  if (m && S[m[1]]) return { id: m[1], text: S[m[1]].n.replace(/ \((V1|V2|V3|C2|C3|C2, C3|mastication|CN VII)\)$/, "") + m[2] };
  return { id: null, text: String(str) };
}
function relIds(id, i) {
  const r = (REL[id] || [])[i]; if (!r) return [];
  return ["d", "s", "p", "w"].flatMap(k => (r[k] || []).map(x => relParts(x).id).filter(Boolean));
}
