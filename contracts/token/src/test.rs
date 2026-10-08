#![cfg(test)]
use super::*;
use soroban_sdk::{testutils::Address as _, Env};

#[test]
fn test_token_initialization_and_metadata() {
    let env = Env::default();
    let contract_id = env.register(NSyncToken, ());
    let client = NSyncTokenClient::new(&env, &contract_id);
    let admin = Address::generate(&env);

    client.initialize(&admin);

    assert_eq!(client.decimals(), 7);
    assert_eq!(client.name(), String::from_str(&env, "NeuroSync Protocol Token"));
    assert_eq!(client.symbol(), String::from_str(&env, "NSYNC"));
}

#[test]
fn test_token_mint_and_balance() {
    let env = Env::default();
    env.mock_all_auths();

    let contract_id = env.register(NSyncToken, ());
    let client = NSyncTokenClient::new(&env, &contract_id);
    let admin = Address::generate(&env);
    let user = Address::generate(&env);

    client.initialize(&admin);

    assert_eq!(client.balance(&user), 0);

    let mint_amount = 1_000_000_000i128; // 100 NSYNC
    client.mint(&user, &mint_amount);

    assert_eq!(client.balance(&user), mint_amount);
}

#[test]
fn test_token_transfer() {
    let env = Env::default();
    env.mock_all_auths();

    let contract_id = env.register(NSyncToken, ());
    let client = NSyncTokenClient::new(&env, &contract_id);
    let admin = Address::generate(&env);
    let alice = Address::generate(&env);
    let bob = Address::generate(&env);

    client.initialize(&admin);
    client.mint(&alice, &500_000_000i128);

    assert_eq!(client.balance(&alice), 500_000_000i128);
    assert_eq!(client.balance(&bob), 0);

    client.transfer(&alice, &bob, &200_000_000i128);

    assert_eq!(client.balance(&alice), 300_000_000i128);
    assert_eq!(client.balance(&bob), 200_000_000i128);
}

#[test]
#[should_panic(expected = "Insufficient balance")]
fn test_transfer_insufficient_balance() {
    let env = Env::default();
    env.mock_all_auths();

    let contract_id = env.register(NSyncToken, ());
    let client = NSyncTokenClient::new(&env, &contract_id);
    let admin = Address::generate(&env);
    let alice = Address::generate(&env);
    let bob = Address::generate(&env);

    client.initialize(&admin);
    client.mint(&alice, &50_000_000i128);

    client.transfer(&alice, &bob, &100_000_000i128);
}

#[test]
#[should_panic(expected = "Already initialized")]
fn test_cannot_reinitialize() {
    let env = Env::default();
    let contract_id = env.register(NSyncToken, ());
    let client = NSyncTokenClient::new(&env, &contract_id);
    let admin1 = Address::generate(&env);
    let admin2 = Address::generate(&env);

    client.initialize(&admin1);
    client.initialize(&admin2);
}
