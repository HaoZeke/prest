extern crate prest;
extern crate rand;

use rand::SeedableRng;
use rand::prng::XorShiftRng;
use prest::{rpc,precomputed,estimation,args,consistency,simulation};
use prest::{experiment_stats,budgetary};
use precomputed::Precomputed;

fn rpc_loop(args : &args::Args) {
    use rpc::*;

    // core state
    let mut rng : XorShiftRng = SeedableRng::from_seed([0;16]);
    let mut rpc = IO::from_stdio();
    let mut precomp = Precomputed::new(
        args.fname_precomputed_preorders.as_ref().map(String::as_str)
    );

    loop {
        let request : ActionRequest = rpc.read().unwrap();

        match request {
            ActionRequest::Quit => {
                break;
            }

            ActionRequest::Echo(msg) => {
                rpc.write_result(Ok::<String, bool>(msg)).unwrap();
            }

            ActionRequest::Crash(msg) => {
                panic!("{}", msg);
            }

            ActionRequest::Fail(msg) => {
                rpc.write_result(Err::<bool, String>(msg)).unwrap();
            }

            ActionRequest::Estimation(req) => {
                rpc.write_result(estimation::run(&mut precomp, &req)).unwrap();
            }

            ActionRequest::Consistency(req) => {
                rpc.write_result(consistency::run(&req)).unwrap();
            }

            ActionRequest::TupleIntransMenus(req) => {
                rpc.write_result(consistency::tuple_intrans::run_menus(&req)).unwrap();
            }

            ActionRequest::TupleIntransAlts(req) => {
                rpc.write_result(consistency::tuple_intrans::run_alts(&req)).unwrap();
            }

            ActionRequest::SetRngSeed(seed) => {
                if seed.len() == 16 {
                    let mut xs = [0u8;16];
                    for (i, &x) in seed.iter().enumerate() {
                        xs[i] = x;
                    }
                    rng = SeedableRng::from_seed(xs);

                    rpc.write_result(Ok::<String, bool>(String::from("OK"))).unwrap();
                } else {
                    rpc.write_result(Err::<bool, String>(
                        String::from("rng seed must contain exactly 16 numbers")
                    )).unwrap();
                }
            }

            ActionRequest::Simulation(req) => {
                rpc.write_result(simulation::run(&mut rng, req)).unwrap();
            }

            ActionRequest::Summary(req) => {
                rpc.write_result(experiment_stats::run(req)).unwrap();
            }

            ActionRequest::BudgetaryConsistency(req) => {
                let resp = budgetary::consistency::run(Logger::new(&mut rpc), req);
                rpc.write_result(resp).unwrap();
            }
        }
    }
}

fn main() {
    let args = args::parse();
    rpc_loop(&args);
}
