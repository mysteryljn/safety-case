#!/usr/bin/env python3
import argparse
import json
from pathlib import Path
def validate(case):
    errors=[]; claims={x.get("id"):x for x in case.get("claims",[])}; evidence={x.get("id"):x for x in case.get("evidence",[])}
    # Node IDs are the names used by references in the argument graph.  A
    # duplicate ID makes a reference ambiguous (and the dictionary
    # comprehensions above silently discard one of the nodes), so reject it
    # instead of validating whichever duplicate happens to come last.
    node_ids=[x.get("id") for x in case.get("claims",[]) + case.get("evidence",[]) if x.get("id")]
    duplicate_ids=[]
    for node_id in node_ids:
        if node_ids.count(node_id) > 1 and node_id not in duplicate_ids:
            duplicate_ids.append(node_id)
    errors.extend("duplicate node id "+str(node_id) for node_id in duplicate_ids)
    # An empty graph cannot constitute a safety argument.  Previously an
    # empty JSON object (or one with no claims) returned ``ok=True`` because
    # there was nothing for the individual checks to reject.
    if not claims:
        errors.append("safety case has no claims")
    for claim in case.get("claims",[]):
        cid=claim.get("id")
        if not cid: errors.append("claim missing id"); continue
        for ref in claim.get("supports",[]):
            if ref not in evidence and ref not in claims: errors.append("%s references missing %s"%(cid,ref))
        if not claim.get("supports"): errors.append("%s has no supporting evidence or subclaim"%cid)
    referenced=set(ref for claim in case.get("claims",[]) for ref in claim.get("supports",[]))
    for eid in evidence:
        if eid not in referenced: errors.append("orphan evidence "+eid)
    graph={cid:[ref for ref in claim.get("supports",[]) if ref in claims] for cid,claim in claims.items()}
    visiting=set(); visited=set()
    def dfs(node):
        if node in visiting: errors.append("cycle detected at "+node); return
        if node in visited: return
        visiting.add(node)
        for child in graph.get(node,[]): dfs(child)
        visiting.remove(node); visited.add(node)
    for cid in graph: dfs(cid)
    return {"claims":len(claims),"evidence":len(evidence),"issues":errors,"ok":not errors}
def main(argv=None):
    p=argparse.ArgumentParser(description="Check a small safety argument graph"); p.add_argument("case",type=Path); a=p.parse_args(argv)
    try: report=validate(json.loads(a.case.read_text(encoding="utf-8")))
    except (OSError,json.JSONDecodeError) as e: print("error: "+str(e)); return 2
    print(json.dumps(report,indent=2,ensure_ascii=False)); return 0 if report["ok"] else 1
if __name__=="__main__": raise SystemExit(main())
