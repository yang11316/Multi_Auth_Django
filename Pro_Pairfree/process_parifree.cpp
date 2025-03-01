#include "process_parifree.h"

/*
    class Process
*/
Process::Process()
{
}

Process::Process(const std::string &acc_publickey, const std::string &acc_cur, const std::string &kgc_P, int nid)
{

    this->acc_cur = mpz_class(acc_cur, 16);
    this->acc_publickey = mpz_class(acc_publickey, 16);

    this->ec_group = EC_GROUP_new_by_curve_name(nid);
    const BIGNUM *order = EC_GROUP_get0_order(ec_group);
    this->q = BN_dup(order);
    this->Pub = crypto_utils::hex2point(this->ec_group, kgc_P);
    this->is_init = true;
}

Process::Process(const std::string &entity_pid, const std::string &acc_publickey, const std::string &acc_cur, const std::string &entity_witness, const std::string &kgc_P, int nid)
{
    this->pid = entity_pid;
    this->acc_witness = mpz_class(entity_witness, 16);
    this->acc_cur = mpz_class(acc_cur, 16);
    this->acc_publickey = mpz_class(acc_publickey, 16);

    this->ec_group = EC_GROUP_new_by_curve_name(nid);
    const BIGNUM *order = EC_GROUP_get0_order(ec_group);
    this->q = BN_dup(order);
    this->Pub = crypto_utils::hex2point(this->ec_group, kgc_P);
    this->is_init = true;
}

Process::Process(const Process &other)
    : acc_cur(other.acc_cur), acc_publickey(other.acc_publickey), acc_witness(other.acc_witness),
      pid(other.pid), is_init(other.is_init), is_fullkey(other.is_fullkey)
{

    // 深拷贝 EC_GROUP
    if (other.ec_group)
    {
        ec_group = EC_GROUP_dup(other.ec_group);
    }
    else
    {
        ec_group = nullptr;
    }

    // 深拷贝 BIGNUM 成员
    q = other.q ? BN_dup(other.q) : nullptr;
    wit_hash = other.wit_hash ? BN_dup(other.wit_hash) : nullptr;
    x = other.x ? BN_dup(other.x) : nullptr;
    wit = other.wit ? BN_dup(other.wit) : nullptr;

    // 深拷贝 EC_POINT 成员
    Pub = other.Pub ? EC_POINT_dup(other.Pub, ec_group) : nullptr;
    X = other.X ? EC_POINT_dup(other.X, ec_group) : nullptr;
    WIT = other.WIT ? EC_POINT_dup(other.WIT, ec_group) : nullptr;
}

Process &Process::operator=(const Process &other)
{
    if (this == &other)
        return *this; // 自我赋值保护

    // 释放旧资源
    if (ec_group)
        EC_GROUP_free(ec_group);
    if (q)
        BN_free(q);
    if (wit_hash)
        BN_free(wit_hash);
    if (x)
        BN_free(x);
    if (wit)
        BN_free(wit);
    if (Pub)
        EC_POINT_free(Pub);
    if (X)
        EC_POINT_free(X);
    if (WIT)
        EC_POINT_free(WIT);

    // 拷贝非指针成员
    acc_cur = other.acc_cur;
    acc_publickey = other.acc_publickey;
    acc_witness = other.acc_witness;
    pid = other.pid;
    is_init = other.is_init;
    is_fullkey = other.is_fullkey;

    // 深拷贝指针成员
    ec_group = other.ec_group ? EC_GROUP_dup(other.ec_group) : nullptr;
    q = other.q ? BN_dup(other.q) : nullptr;
    wit_hash = other.wit_hash ? BN_dup(other.wit_hash) : nullptr;
    x = other.x ? BN_dup(other.x) : nullptr;
    wit = other.wit ? BN_dup(other.wit) : nullptr;
    Pub = other.Pub ? EC_POINT_dup(other.Pub, ec_group) : nullptr;
    X = other.X ? EC_POINT_dup(other.X, ec_group) : nullptr;
    WIT = other.WIT ? EC_POINT_dup(other.WIT, ec_group) : nullptr;

    return *this;
}

Process::~Process()
{

    if (ec_group)
    {
        EC_GROUP_free(ec_group);
        ec_group = nullptr;
    }
    if (Pub)
    {
        EC_POINT_free(Pub);
        Pub = nullptr;
    }
    if (X)
    {
        EC_POINT_free(X);
        X = nullptr;
    }
    if (WIT)
    {
        EC_POINT_free(WIT);
        WIT = nullptr;
    }
    if (q)
    {
        BN_free(q);
        q = nullptr;
    }
    if (wit_hash)
    {
        BN_free(wit_hash);
        wit_hash = nullptr;
    }
    if (x)
    {
        BN_free(x);
        x = nullptr;
    }
    if (wit)
    {
        BN_free(wit);
        wit = nullptr;
    }
}

void Process::init(const std::string &entity_pid, const std::string &acc_publickey, const std::string &acc_cur, const std::string &kgc_P, int nid)
{
    this->pid = entity_pid;
    this->acc_cur = mpz_class(acc_cur, 16);
    this->acc_publickey = mpz_class(acc_publickey, 16);
    this->ec_group = EC_GROUP_new_by_curve_name(nid);
    const BIGNUM *order = EC_GROUP_get0_order(ec_group);
    this->q = BN_dup(order);
    this->Pub = crypto_utils::hex2point(this->ec_group, kgc_P);
    this->is_init = true;
}
void Process::init(const std::string &entity_pid, const std::string &acc_publickey, const std::string &acc_cur, const std::string &entity_witness, const std::string &kgc_P, int nid)
{
    try
    {
        this->pid = entity_pid;
        this->acc_witness = mpz_class(entity_witness, 16);
        this->acc_cur = mpz_class(acc_cur, 16);
        this->acc_publickey = mpz_class(acc_publickey, 16);

        this->ec_group = EC_GROUP_new_by_curve_name(nid);
        const BIGNUM *order = EC_GROUP_get0_order(ec_group);
        this->q = BN_dup(order);
        this->Pub = crypto_utils::hex2point(this->ec_group, kgc_P);
        this->is_init = true;
    }
    catch (const std::exception &e)
    {
        std::cerr << e.what() << '\n';
    }
}

bool Process::verify_member(const mpz_class &entity_pid, const mpz_class &entity_witness, const mpz_class &h1)
{
    mpz_class rhs;
    mpz_class acc_hex;
    mpz_powm(rhs.get_mpz_t(), entity_witness.get_mpz_t(), entity_pid.get_mpz_t(),
             this->acc_publickey.get_mpz_t());

    mpz_powm(acc_hex.get_mpz_t(), this->acc_cur.get_mpz_t(), h1.get_mpz_t(),
             this->acc_publickey.get_mpz_t());
    std::cout << "acc:" << this->acc_cur.get_str(16) << std::endl;

    return acc_hex == rhs;
}

void Process::update_witness(const mpz_class &aux)
{
    mpz_powm(acc_witness.get_mpz_t(), acc_witness.get_mpz_t(), aux.get_mpz_t(),
             acc_publickey.get_mpz_t());
}
void Process::update_accumulator(const mpz_class &aux)
{

    mpz_powm(acc_cur.get_mpz_t(), acc_cur.get_mpz_t(), aux.get_mpz_t(),
             acc_publickey.get_mpz_t());
}
bool Process::generate_full_key()
{
    try
    {
        // sk = (x,wit)
        BIGNUM *x = BN_new();
        BN_rand_range(x, this->q);
        this->x = x;

        BIGNUM *wit = crypto_utils::hex2bn(this->acc_witness.get_str(16));
        this->wit = wit;

        // pk = (X,WIT,wit^hex)
        // X = x * P
        EC_POINT *X = EC_POINT_new(this->ec_group);
        EC_POINT_mul(this->ec_group, X, x, nullptr, nullptr, nullptr);
        // WIT = wip*P
        EC_POINT *WIT = EC_POINT_new(this->ec_group);
        EC_POINT_mul(this->ec_group, WIT, wit, nullptr, nullptr, nullptr);

        // h1(pid,WIT,X)
        BIGNUM *h1_str = crypto_utils::string2hash2bn(this->pid + crypto_utils::point2hex(this->ec_group, WIT) + crypto_utils::point2hex(this->ec_group, X));
        mpz_class mpz_h1 = mpz_class(crypto_utils::bn2hex(h1_str), 16);
        mpz_class tmp = crypto_utils::quick_pow(this->acc_witness, mpz_h1, this->acc_publickey);
        BIGNUM *wit_hash = crypto_utils::hex2bn(tmp.get_str(16));

        this->X = X;
        this->WIT = WIT;
        this->wit_hash = wit_hash;

        BN_free(h1_str);
        this->is_fullkey = true;

        return true;
    }
    catch (const std::exception &e)
    {
        std::cerr << e.what() << '\n';
        return false;
    }
}

sign_payload Process::sign(const std::string &msg)
{
    struct timeval begtime, endtime;
    gettimeofday(&begtime, NULL);

    BN_CTX *bn_ctx = BN_CTX_new();

    // timestamp ti
    std::string ti = crypto_utils::getTimeStamp();

    // randomly choose number y
    BIGNUM *y = BN_new();
    BN_rand_range(y, this->q);
    // Y = y*P
    EC_POINT *Y = EC_POINT_new(this->ec_group);
    EC_POINT_mul(this->ec_group, Y, y, nullptr, nullptr, nullptr);

    // u = hash(m,PID,PK,t,Y)
    std::string u_str = msg + this->pid + crypto_utils::point2hex(this->ec_group, this->X) + crypto_utils::point2hex(this->ec_group, this->WIT) + crypto_utils::bn2hex(this->wit_hash) + ti + crypto_utils::point2hex(this->ec_group, Y);
    BIGNUM *u = crypto_utils::string2hash2bn(u_str);

    // h3 = hash(m,pid,pk,t)
    std::string h3_str = msg + this->pid + crypto_utils::point2hex(this->ec_group, this->X) + crypto_utils::point2hex(this->ec_group, this->WIT) + crypto_utils::bn2hex(this->wit_hash) + ti;
    BIGNUM *h3 = crypto_utils::string2hash2bn(h3_str);

    // h4 = hash(m,pid,Pub,t)
    std::string h4_str = msg + this->pid + crypto_utils::point2hex(this->ec_group, this->Pub) + ti;
    BIGNUM *h4 = crypto_utils::string2hash2bn(h4_str);

    // w = u*y + h3*x + h4*wit

    BIGNUM *w = BN_new();
    BIGNUM *tmp = BN_new();

    // u*y
    BN_mod_mul(tmp, u, y, this->q, bn_ctx);
    // h3*x
    BN_mod_mul(w, h3, this->x, this->q, bn_ctx);
    // u*y + h3*x
    BN_mod_add(w, w, tmp, this->q, bn_ctx);
    // h4*wit
    BN_mod_mul(tmp, h4, this->wit, this->q, bn_ctx);
    // w = u*y + h3*x + h4*wit
    BN_mod_add(w, w, tmp, this->q, bn_ctx);
    sign_payload payload = {
        this->pid,
        msg,
        crypto_utils::point2hex(this->ec_group, this->X),
        crypto_utils::point2hex(this->ec_group, this->WIT),
        crypto_utils::bn2hex(this->wit_hash),
        crypto_utils::point2hex(this->ec_group, Y),
        crypto_utils::bn2hex(w),
        ti};
    BN_free(tmp);
    BN_free(w);
    BN_free(h4);
    BN_free(h3);
    BN_free(u);
    BN_free(y);
    EC_POINT_free(Y);
    BN_CTX_free(bn_ctx);
    gettimeofday(&endtime, NULL);

    long timeuse = 1000000 * (endtime.tv_sec - begtime.tv_sec) + endtime.tv_usec - begtime.tv_usec;
    printf("sign time: %ld us\n", timeuse);
    return payload;
}

bool Process::verify_sign(const sign_payload &payload)
{
    struct timeval begtime, acc_time, cls_time;

    BN_CTX *bn_ctx = BN_CTX_new();
    // u = hash(m,PID,PK,t,Y)
    std::string u_str = payload.msg + payload.pid + payload.X + payload.WIT + payload.wit_hex + payload.time_stamp + payload.sig1;
    BIGNUM *u = crypto_utils::string2hash2bn(u_str);

    // h3 = hash(m,pid,pk,t)
    std::string h3_str = payload.msg + payload.pid + payload.X + payload.WIT + payload.wit_hex + payload.time_stamp;
    BIGNUM *h3 = crypto_utils::string2hash2bn(h3_str);

    // h4 = hash(m,pid,Pub,t)
    std::string h4_str = payload.msg + payload.pid + crypto_utils::point2hex(this->ec_group, this->Pub) + payload.time_stamp;
    BIGNUM *h4 = crypto_utils::string2hash2bn(h4_str);

    // h1 = hash(pid,WIT,X)
    BIGNUM *h1 = crypto_utils::string2hash2bn(payload.pid + payload.WIT + payload.X);

    // 首先进行累加器验证
    mpz_class entity_pid = mpz_class(payload.pid, 16);
    mpz_class h1_mpz = mpz_class(crypto_utils::bn2hex(h1), 16);
    mpz_class wit_hex = mpz_class(payload.wit_hex, 16);

    // 累加器验证
    gettimeofday(&begtime, NULL);
    if (!this->verify_member(entity_pid, wit_hex, h1_mpz))
    {
        std::cout << "[INVALID]accumulator wrong" << std::endl;
        BN_free(h1);
        BN_free(h4);
        BN_free(h3);
        BN_free(u);
        BN_CTX_free(bn_ctx);
        return false;
    }
    gettimeofday(&acc_time, NULL);
    // 进行签名验证
    // w*P == u*Y + h3*X + h4*WIT
    // w*P
    BIGNUM *w = crypto_utils::hex2bn(payload.sig2);
    EC_POINT *lhs = EC_POINT_new(this->ec_group);

    EC_POINT_mul(this->ec_group, lhs, w, nullptr, nullptr, bn_ctx);

    // u*Y + h3*X + h4*WIT
    EC_POINT *rhs = EC_POINT_new(this->ec_group);
    EC_POINT *tmp_rhs = EC_POINT_new(this->ec_group);
    EC_POINT *Y = crypto_utils::hex2point(this->ec_group, payload.sig1);
    EC_POINT *X = crypto_utils::hex2point(this->ec_group, payload.X);
    EC_POINT *WIT = crypto_utils::hex2point(this->ec_group, payload.WIT);
    EC_POINT_mul(this->ec_group, rhs, nullptr, Y, u, bn_ctx);
    EC_POINT_mul(this->ec_group, tmp_rhs, nullptr, X, h3, bn_ctx);

    // u*Y + h3*X

    EC_POINT_add(this->ec_group, rhs, rhs, tmp_rhs, bn_ctx);
    EC_POINT_mul(this->ec_group, tmp_rhs, nullptr, WIT, h4, bn_ctx);
    EC_POINT_add(this->ec_group, rhs, rhs, tmp_rhs, bn_ctx);

    gettimeofday(&cls_time, NULL);
    // long acc_timeuse = 1000000 * (acc_time.tv_sec - begtime.tv_sec) + acc_time.tv_usec - begtime.tv_usec;
    // long cls_timeuse = 1000000 * (cls_time.tv_sec - acc_time.tv_sec) + cls_time.tv_usec - acc_time.tv_usec;
    long verify_timeuse = 1000000 * (cls_time.tv_sec - begtime.tv_sec) + cls_time.tv_usec - begtime.tv_usec;
    // printf("acc verify time: %ld us\n", acc_timeuse);
    // printf("cls verify time: %ld us\n", cls_timeuse);
    printf("verify time: %ld us\n", verify_timeuse);

    if (EC_POINT_cmp(this->ec_group, lhs, rhs, nullptr) != 0)
    {
        std::cout << "[INVALID]signature wrong" << std::endl;
        BN_free(h1);
        BN_free(h4);
        BN_free(h3);
        BN_free(u);
        BN_free(w);
        EC_POINT_free(lhs);
        EC_POINT_free(rhs);
        EC_POINT_free(tmp_rhs);
        EC_POINT_free(Y);
        EC_POINT_free(X);
        EC_POINT_free(WIT);
        BN_CTX_free(bn_ctx);
        return false;
    }
    else
    {
        BN_free(h1);
        BN_free(h4);
        BN_free(h3);
        BN_free(u);
        BN_free(w);
        EC_POINT_free(lhs);
        EC_POINT_free(rhs);
        EC_POINT_free(tmp_rhs);
        EC_POINT_free(Y);
        EC_POINT_free(X);
        EC_POINT_free(WIT);
        BN_CTX_free(bn_ctx);
        std::cout << "[SUCESS]sign verify sucessfully" << std::endl;
        return true;
    }
}

void Process::update_key(const std::string &aux)
{
    try
    {
        struct timeval begtime, endtime;
        gettimeofday(&begtime, NULL);
        // std::cout << "update key" << std::endl;
        mpz_class aux_mpz = mpz_class(aux, 16);
        // update witness
        this->update_witness(aux_mpz);
        // update accumylator
        this->update_accumulator(aux_mpz);

        // update private key
        // free the old key
        BN_free(this->wit);
        BIGNUM *wit_new = crypto_utils::hex2bn(this->acc_witness.get_str(16));
        this->wit = wit_new;

        // update public key
        // WIT = wit*P
        EC_POINT *WIT_new = EC_POINT_new(this->ec_group);
        EC_POINT_mul(this->ec_group, WIT_new, wit_new, nullptr, nullptr, nullptr);
        // h1(pid,WIT,X)
        BIGNUM *h1_str = crypto_utils::string2hash2bn(this->pid + crypto_utils::point2hex(this->ec_group, WIT_new) + crypto_utils::point2hex(this->ec_group, this->X));
        mpz_class mpz_h1 = mpz_class(crypto_utils::bn2hex(h1_str), 16);
        mpz_class tmp = crypto_utils::quick_pow(this->acc_witness, mpz_h1, this->acc_publickey);
        BIGNUM *wit_hash_new = crypto_utils::hex2bn(tmp.get_str(16));
        BN_free(h1_str);
        EC_POINT_free(this->WIT);
        BN_free(this->wit_hash);
        this->WIT = WIT_new;
        this->wit_hash = wit_hash_new;
        gettimeofday(&endtime, NULL);
        long update_timeuse = 1000000 * (endtime.tv_sec - begtime.tv_sec) + endtime.tv_usec - begtime.tv_usec;

        printf("update time: %ld us\n", update_timeuse);
    }
    catch (const std::exception &e)
    {
        std::cerr << "update key:" << e.what() << '\n';
    }
}

/*
    class Process_manager
    将process进行封装
*/

Process_manager::~Process_manager()
{
    process_vec.clear();
}

void Process_manager::push_back(Process &tmp_process)
{
    this->process_vec.push_back({tmp_process.pid, false});
    this->process_unmap.insert({tmp_process.pid, tmp_process});
    this->size++;
}

std::string Process_manager::get_alivable_process()
{

    for (int i = 0; i < this->size; i++)
    {
        if (this->process_vec[i].second == false)
        {
            std::string pid = this->process_vec[i].first;
            this->process_vec[i].second = true;
            this->used_index = i;
            return pid;
        }
    }

    return std::string();
}

sign_payload Process_manager::sign(const std::string &pid, const std::string &msg)
{
    if (this->process_unmap.find(pid) != this->process_unmap.end())
    {
        return this->process_unmap[pid].sign(msg);
    }
    std::cout << "[ERROR] no such pid" << std::endl;
    return sign_payload();
}

bool Process_manager::verify_sign(const std::string &pid, const sign_payload &payload)
{
    if (this->process_unmap.find(pid) != this->process_unmap.end())
    {
        return this->process_unmap[pid].verify_sign(payload);
    }
    std::cout << "[ERROR] no such pid" << std::endl;
    return false;
}

bool Process_manager::delete_process(const std::string &pid)
{
    try
    {
        for (int i = 0; i < this->size; i++)
        {
            if (this->process_vec[i].first == pid)
            {
                if (i <= this->used_index)
                {
                    this->used_index--;
                }
                this->process_vec.erase(this->process_vec.begin() + i);
                this->process_unmap.erase(pid);
                this->size--;
                return true;
            }
        }
        std::cout << "delete process not find " << std::endl;
        return false;
    }
    catch (const std::exception &e)
    {
        std::cerr << e.what() << '\n';
        return false;
    }
}

bool Process_manager::update_process(const std::string &aux)
{
    try
    {
        for (auto tmp_pair : this->process_vec)
        {
            this->process_unmap[tmp_pair.first].update_key(aux);
        }
        return true;
    }
    catch (const std::exception &e)
    {
        std::cerr << e.what() << '\n';
        return false;
    }
}

int Process_manager::get_available_size()
{
    return this->size - this->used_index - 1;
}

int Process_manager::get_size()
{
    return this->size;
}

bool Process_manager::has_process(const std::string &pid)
{
    if (this->process_unmap.find(pid) != this->process_unmap.end())
    {
        return true;
    }

    return false;
}
